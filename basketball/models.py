"""
basketball app: INPUT data ke models.

Ye models raw dump (bball_raw database) ki saaf copy hain. Inhein sirf
`import_raw` management command bharti hai. Koi calculation yahan nahi hoti;
calculations analytics app mein hain.

Design rules (dekhein ASSUMPTIONS.md):
  D-01  Har model ka primary key Django ka auto `id` hai. ESPN ki ids alag
        unique fields hain (espn_team_id, espn_player_id, espn_game_id).
  D-02  Composite primary key nahi, lekin duplicate rokne ke liye
        composite UNIQUE constraints hain.
  D-03  Season ka koi model nahi; har jagah SmallIntegerField (jaise 2026).
  D-09  Possession ke player columns par index nahi (2.36M rows).
  D-10  Har source table ka apna model (counts, possessions, box, torvik).
  D-15  Input data ke saare ForeignKeys PROTECT hain: ghalti se delete
        karne par history nahi urti.
  D-17  Raw `numeric` columns DecimalField hain taake copy lossless rahe.
"""
from django.db import models

from .choices import REGULAR_SEASON_TYPE, Zone


# ---------------------------------------------------------------------------
# Teams aur players
# ---------------------------------------------------------------------------

class Team(models.Model):
    """
    Ek college team, saare seasons ke liye ek hi row.

    Jo cheez season ke saath badalti hai (conference) woh TeamSeason mein hai.
    """
    espn_team_id = models.IntegerField(
        unique=True,
        help_text="ESPN ki team id (raw: teams.team_id).",
    )
    name = models.CharField(
        max_length=200,
        help_text="Team ka naam (import ke waqt sab se naye season wala).",
    )

    def __str__(self):
        return f"{self.name} ({self.espn_team_id})"


class TeamSeason(models.Model):
    """
    Ek team ka ek season. Is ka asal kaam: batana ke us season team D1 thi ya nahi.

    Spec: "D1 team = ESPN ne us season conference id di ho (independents shamil)".
    Replacement level aur points per win sirf D1 teams par bante hain.
    """
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="seasons",
        help_text="Kaunsi team.",
    )
    season = models.SmallIntegerField(
        help_text="Season ka saal, jaise 2026 (2025-26 season).",
    )
    conference_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ESPN conference id. NULL ka matlab us season team D1 nahi thi.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "season"], name="uniq_teamseason_team_season"
            ),
        ]

    @property
    def is_d1(self):
        """True agar us season team ke paas conference id thi (spec ki D1 definition)."""
        return self.conference_id is not None

    def __str__(self):
        return f"{self.team.name} {self.season}"


class Player(models.Model):
    """Ek player, saare seasons ke liye ek row."""
    espn_player_id = models.IntegerField(
        unique=True,
        help_text="ESPN ki athlete id (raw: players.player_id).",
    )
    name = models.CharField(max_length=200, help_text="Player ka naam.")

    def __str__(self):
        return f"{self.name} ({self.espn_player_id})"


# ---------------------------------------------------------------------------
# Games aur possessions
# ---------------------------------------------------------------------------

class GameQuerySet(models.QuerySet):
    """Game ke reusable filters."""

    def regular_season(self):
        """
        Spec ka "regular season": season_type = 2, koi tournament id nahi,
        aur game mukammal ho chuka ho.

        Ye filter code mein SIRF yahin likha hai (D-14). Har jagah
        `Game.objects.regular_season()` use karein, filter dobara mat likhein.
        Dev data mein: 18,866 games -> 16,665 regular (F-05).
        """
        return self.filter(
            season_type=REGULAR_SEASON_TYPE,
            tournament_id__isnull=True,
            is_completed=True,
        )

    def for_season(self, season):
        """Ek season ke games."""
        return self.filter(season=season)


class Game(models.Model):
    """
    Ek match. Postseason aur conference tournament games bhi table mein hain;
    calculations unhein regular_season() se bahar karti hain.
    """
    espn_game_id = models.BigIntegerField(
        unique=True,
        help_text="ESPN game id (raw: games.game_id).",
    )
    season = models.SmallIntegerField(db_index=True, help_text="Season ka saal.")
    game_date = models.DateField(help_text="Match ki tareekh.")
    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="home_games",
        help_text="Ghar wali team.",
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="away_games",
        help_text="Mehmaan team.",
    )
    season_type = models.SmallIntegerField(
        help_text="ESPN code: 2 = regular season (conference tournaments bhi), 3 = postseason.",
    )
    tournament_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Agar tournament (jaise conference tournament) ka game hai to us ki id. "
                  "Regular season games mein NULL.",
    )
    has_shot_tags = models.BooleanField(
        help_text="ESPN ke naye feed ke shot tags (driving, pull-up, floater...) is game mein hain ya nahi.",
    )
    is_completed = models.BooleanField(help_text="Game khatam ho chuka hai ya nahi.")
    home_score = models.SmallIntegerField(
        null=True, blank=True, help_text="Final score (ghar wali team)."
    )
    away_score = models.SmallIntegerField(
        null=True, blank=True, help_text="Final score (mehmaan team)."
    )

    objects = GameQuerySet.as_manager()

    @property
    def is_regular_season(self):
        """Ek game ke liye wahi check jo GameQuerySet.regular_season() karta hai."""
        return (
            self.season_type == REGULAR_SEASON_TYPE
            and self.tournament_id is None
            and self.is_completed
        )

    def __str__(self):
        return f"{self.espn_game_id} ({self.game_date})"


class Possession(models.Model):
    """
    Ek possession (jab tak ek team ke paas ball rahi) aur us waqt court par
    dono teams ke 5-5 players. Role ke teammate shares (lead, inside, front)
    isi se bante hain.

    Ye sab se bari table hai (dev mein ~2.36M rows). Is liye:
      - player columns par index nahi (D-09); calculation poori season ek
        saath parhti hai, kabhi ek player se filter nahi karti.
      - related_name="+" ka matlab: Player/Team par ulta rishta mat banao.
        Ek hi model ki taraf 10 FKs hain; warna Django naam takrane ka error deta.
    """
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        db_index=False,  # unique (game, possession_no) ka index pehle se game se shuru hota hai
        related_name="possessions",
        help_text="Kis game ka possession.",
    )
    possession_no = models.IntegerField(help_text="Game ke andar possession ka number.")
    season = models.SmallIntegerField(
        db_index=True,
        help_text="Season (game.season ki copy, taake season-wise parhna tez ho).",
    )
    off_team = models.ForeignKey(
        Team, on_delete=models.PROTECT, db_index=False, related_name="+",
        help_text="Attack karne wali team.",
    )
    def_team = models.ForeignKey(
        Team, on_delete=models.PROTECT, db_index=False, related_name="+",
        help_text="Defend karne wali team.",
    )

    # Offense ke 5 players (order ka koi matlab nahi). NULL = lineup resolve nahi hui.
    off_p1 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    off_p2 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    off_p3 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    off_p4 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    off_p5 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")

    # Defense ke 5 players.
    def_p1 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    def_p2 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    def_p3 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    def_p4 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")
    def_p5 = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True, db_index=False, related_name="+")

    garbage_time = models.BooleanField(
        help_text="True = match ka faisla ho chuka tha; spec ke mutabiq ye possession gina nahi jata.",
    )
    off_five_distinct = models.BooleanField(
        help_text="Offense ke 5 alag alag players resolve hue. False ho to offense ke liye ye possession nahi ginta.",
    )
    def_five_distinct = models.BooleanField(
        help_text="Defense ke 5 alag alag players resolve hue.",
    )

    # Helper ke liye field names ki list (copy-paste se bachne ke liye).
    OFF_PLAYER_FIELDS = ("off_p1_id", "off_p2_id", "off_p3_id", "off_p4_id", "off_p5_id")
    DEF_PLAYER_FIELDS = ("def_p1_id", "def_p2_id", "def_p3_id", "def_p4_id", "def_p5_id")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["game", "possession_no"], name="uniq_possession_game_no"
            ),
        ]

    def offense_player_ids(self):
        """Offense ke player ids (Django id, ESPN nahi). NULL wale chhor diye jate hain."""
        return [pid for pid in (getattr(self, f) for f in self.OFF_PLAYER_FIELDS) if pid is not None]

    def defense_player_ids(self):
        """Defense ke player ids (Django id). NULL wale chhor diye jate hain."""
        return [pid for pid in (getattr(self, f) for f in self.DEF_PLAYER_FIELDS) if pid is not None]

    @property
    def counts_for_offense(self):
        """Spec: possession tab ginta hai jab side ke 5 distinct players hon aur garbage time na ho."""
        return self.off_five_distinct and not self.garbage_time

    @property
    def counts_for_defense(self):
        """Defense side ke liye wahi rule."""
        return self.def_five_distinct and not self.garbage_time

    def __str__(self):
        return f"Game {self.game_id} #{self.possession_no}"


# ---------------------------------------------------------------------------
# Player-season data (har source ka apna model, D-10)
# ---------------------------------------------------------------------------

class PlayerSeasonBase(models.Model):
    """
    Charon player-season models ka common hissa: player, season, team, aur
    "ek player ka ek season mein ek hi row" wala unique constraint.

    abstract = True: is ki apni koi table nahi banti; sirf neeche ke models
    in fields ko inherit karte hain.
    """
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="%(class)s_set",  # jaise player.playerseasoncounts_set
        help_text="Kaunsa player.",
    )
    season = models.SmallIntegerField(db_index=True, help_text="Season ka saal.")
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="%(class)s_set",
        help_text="Is season player ki team.",
    )

    class Meta:
        abstract = True
        constraints = [
            # %(class)s har model ka apna naam daal deta hai, taake constraint
            # ka naam har table ke liye alag ho.
            models.UniqueConstraint(
                fields=["player", "season"], name="uniq_%(class)s_player_season"
            ),
        ]

    def __str__(self):
        return f"{self.player_id} {self.season}"


class PlayerSeasonCounts(PlayerSeasonBase):
    """
    Play-by-play se gine gaye counts, ek player-season ke liye (raw: player_season_counts).

    Role aur Level dono ka core input. Sirf regular season (F-07).
    Sirf COUNTS hain, rates nahi; rates analytics mein possessions se bante hain.

    Tagged columns (driving_layups ... alley_oops) sirf 2026 jaise seasons mein
    bhare hain jahan ESPN shot tags dete hain. Pehle ke seasons mein NULL.
    Note (A-10): 2026 mein bhi agar player ka koi tagged game nahi
    (tagged_off_poss = 0), to raw mein 0 likha hai lekin calculation inhein
    NULL treat karti hai. Ye model raw jaisa hi rakhta hai.
    """
    # --- Creation (doosron ke liye moqa banana) ---
    assists = models.IntegerField(help_text="Kul assists (pass jis ke baad teammate ne score kiya).")
    ast_to_three = models.IntegerField(help_text="Woh assists jin par 3-pointer bana.")
    ast_to_rim = models.IntegerField(help_text="Woh assists jin par rim shot bana. Mid-range assists = assists - ast_to_three - ast_to_rim (A-05).")

    # --- Self-creation ---
    ft_trips = models.IntegerField(help_text="Free throw trips: ek hi waqt (same game, same clock) ke FTs = 1 trip.")
    transition_fga = models.IntegerField(help_text="Team ke defensive rebound ya steal ke 8 second ke andar liye gaye shots.")

    # --- Defense ---
    steals = models.IntegerField(help_text="Ball cheenna.")
    blocks = models.IntegerField(help_text="Shot rokna.")
    drb = models.IntegerField(help_text="Defensive rebounds.")

    # --- Inside ---
    orb = models.IntegerField(help_text="Offensive rebounds (apni team ki miss wapas lena).")
    putbacks = models.IntegerField(help_text="Apne offensive rebound ke 3 second ke andar us ka shot.")

    # --- Shots by zone (FGA = attempts, FGM = makes, _ast = assisted makes) ---
    fga_rim = models.IntegerField(help_text="Rim attempts.")
    fgm_rim = models.IntegerField(help_text="Rim makes.")
    fgm_rim_ast = models.IntegerField(help_text="Rim makes jin par assist tha.")
    fga_mid = models.IntegerField(help_text="Mid-range 2 attempts.")
    fgm_mid = models.IntegerField(help_text="Mid-range 2 makes.")
    fgm_mid_ast = models.IntegerField(help_text="Mid-range makes jin par assist tha.")
    fga_three = models.IntegerField(help_text="3-point attempts.")
    fgm_three = models.IntegerField(help_text="3-point makes.")
    fgm_three_ast = models.IntegerField(help_text="3-point makes jin par assist tha.")

    # --- Free throws ---
    fta = models.IntegerField(help_text="Free throw attempts.")
    ftm = models.IntegerField(help_text="Free throws made.")

    # --- Level-only counts ---
    turnovers = models.IntegerField(help_text="Ball ganwana (Level: Ball security).")
    fts_conceded = models.IntegerField(help_text="Is player ke fouls par opponent ko mile free throws (Level: Discipline).")
    technicals = models.IntegerField(help_text="Technical fouls. A-07: offsetting pehle se nikle hue maane gaye hain.")

    # --- 2026 tagged play types (NULL jahan season mein tags nahi) ---
    driving_layups = models.IntegerField(null=True, blank=True, help_text="Tagged: dribble kar ke layup.")
    pullups_2 = models.IntegerField(null=True, blank=True, help_text="Tagged: pull-up / step-back 2s.")
    pullup_range_2s = models.IntegerField(null=True, blank=True, help_text="10 ft se bahar ke mid-range 2s (hook nahi). Rate poori season ke off_poss par (A-11).")
    floaters = models.IntegerField(null=True, blank=True, help_text="Tagged: floater shots.")
    pullups_3 = models.IntegerField(null=True, blank=True, help_text="Tagged: pull-up / step-back 3s.")
    plain_rim_fga = models.IntegerField(null=True, blank=True, help_text="Tagged games: bina khaas tag ke rim attempts (cut & roll ke liye).")
    plain_rim_fgm = models.IntegerField(null=True, blank=True, help_text="Tagged games: plain rim makes.")
    plain_rim_fgm_ast = models.IntegerField(null=True, blank=True, help_text="Tagged games: assisted plain rim makes.")
    tip_ins = models.IntegerField(null=True, blank=True, help_text="Tagged: tip-ins.")
    hooks_turnarounds = models.IntegerField(null=True, blank=True, help_text="Tagged: hook / turnaround shots (post moves).")
    alley_oops = models.IntegerField(null=True, blank=True, help_text="Tagged: lobs. Gine jate hain lekin abhi kisi group mein nahi.")

    class Meta(PlayerSeasonBase.Meta):
        verbose_name_plural = "player season counts"

    @property
    def ast_to_mid(self):
        """Mid-range assists. Schema mein column nahi, is liye nikalte hain (A-05, F-09)."""
        return self.assists - self.ast_to_three - self.ast_to_rim

    @property
    def pbp_points(self):
        """Play-by-play ke mutabiq us ke points. Level ka coverage = pbp_points / box points."""
        return 2 * self.fgm_rim + 2 * self.fgm_mid + 3 * self.fgm_three + self.ftm


class PlayerSeasonPossessions(PlayerSeasonBase):
    """
    Player court par kitne possessions raha (raw: player_season_possessions).
    Ye rates ke denominator hain: rate = count / possessions * 100.
    """
    off_poss = models.IntegerField(help_text="Offensive possessions jab woh court par tha. Offense ke rates isi par.")
    def_poss = models.IntegerField(help_text="Defensive possessions. Steals, blocks, def. rebounds ke rates isi par.")
    tagged_off_poss = models.IntegerField(
        null=True, blank=True,
        help_text="Sirf shot-tag wale games ke offensive possessions. Tagged play types ke rates isi par. "
                  "0 ya NULL = tagged values blank (A-10).",
    )

    class Meta(PlayerSeasonBase.Meta):
        verbose_name_plural = "player season possessions"


class PlayerSeasonBox(PlayerSeasonBase):
    """Box score se minutes aur points (raw: player_season_box). Level ke liye."""
    minutes = models.IntegerField(help_text="Regular-season minutes (ESPN box). EPA/40 ka denominator.")
    points = models.IntegerField(help_text="Box-score points. Coverage ka denominator.")

    class Meta(PlayerSeasonBase.Meta):
        verbose_name_plural = "player season box"


class TorvikPlayerSeason(PlayerSeasonBase):
    """
    Torvik (barttorvik.com) ke season stats (raw: torvik_player_season).
    Torvik sirf D1 players cover karta hai (F-13).

    Role ke liye: height_in, min_pct, usage, three_pa_share.
    Baaqi columns Step 3 (Impact on Winning) ke liye abhi se import hote hain.
    """
    height_in = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        help_text="Height inches mein (half-inch mumkin, F-14). 77.0 = 6'5\", 80.0 = 6'8\".",
    )
    min_pct = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Team ke minutes ka kitna % khela (0-100). Qualified = 40 ya zyada.",
    )
    usage = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Usage %: team ke possessions mein se kitne is ke haath khatam hue.",
    )
    three_pa_share = models.DecimalField(
        max_digits=5, decimal_places=4,
        help_text="Shots ka kitna hissa 3-pointers (0-1). Shooting rule: 0.60+ = 3pt Specialist (A-13).",
    )

    # --- Step 3 (Impact) ke liye; abhi istemal nahi ---
    to_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Turnover %.")
    stl_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Steal %.")
    blk_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Block %.")
    orb_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Offensive rebound %.")
    ast_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Assist %.")
    fouls_per_40 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Fouls per 40 minutes.")
    bpm = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True, help_text="Box Plus/Minus.")

    class Meta(PlayerSeasonBase.Meta):
        verbose_name_plural = "torvik player seasons"


# ---------------------------------------------------------------------------
# League-wide input
# ---------------------------------------------------------------------------

class NationalAssistShare(models.Model):
    """
    Har season aur zone ke liye poore mulk ka assisted share (assisted makes / makes).

    Player ka apna assisted share is ki taraf "shrink" hota hai:
        a = (his assisted makes + 5 * national share) / (his makes + 5)
    """
    season = models.SmallIntegerField(help_text="Season ka saal.")
    zone = models.CharField(max_length=10, choices=Zone.choices, help_text="Shot zone.")
    ast_share = models.DecimalField(
        max_digits=6, decimal_places=4,
        help_text="National assisted share (0-1).",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["season", "zone"], name="uniq_nationalassistshare_season_zone"
            ),
        ]

    def __str__(self):
        return f"{self.season} {self.zone}: {self.ast_share}"