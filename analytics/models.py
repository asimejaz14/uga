"""
analytics app: CALCULATED results ke models.

Inhein sirf compute commands (compute_role, compute_level) bharti hain.
API (api app) inhein sirf PARHTI hai; API request ke andar kabhi
calculation nahi hoti (D-07).

Design rules (dekhein ASSUMPTIONS.md):
  D-06  Har calculation ek CalculationRun hai. Saare results apni run se
        jure hain. API hamesha is season + kind ki latest SUCCESS run parhti hai.
  D-15  Result -> run FK CASCADE hai (purani run delete = us ke results bhi).
        Result -> player/team FK PROTECT hai.
  D-17  Calculated numbers FloatField hain (rounding sirf display par).
  D-18  Result rows par season nahi; season run par hai (run__season).
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from basketball.models import Player, Team

from .choices import (
    Confidence, DecidedBy, Family, Group, Role, RulesMode, RunKind,
    RunStatus, Sample, Tier,
)
from .constants import SPEC_VERSION


# ---------------------------------------------------------------------------
# Calculation runs
# ---------------------------------------------------------------------------

class CalculationRunQuerySet(models.QuerySet):

    def successful(self):
        """Sirf woh runs jo poori kamyabi se khatam hui."""
        return self.filter(status=RunStatus.SUCCESS)

    def latest_success(self, kind, season):
        """
        Is season aur kind ki sab se nayi kamyab run, ya None.

        API ka "latest valid result" yahi hai (D-06). Nayi run chal rahi ho
        ya fail ho jaye, tab bhi ye purani kamyab run hi deta hai.
        """
        return (
            self.successful()
            .filter(kind=kind, season=season)
            .order_by("-finished_at", "-id")
            .first()
        )

    def latest_success_per_season(self, kind):
        """
        Har season ki latest kamyab run, {season: run} ki shakal mein.
        Player ki saari seasons ki history wali API ke liye kaam aayega.
        """
        latest = {}
        for run in self.successful().filter(kind=kind).order_by("season", "finished_at", "id"):
            latest[run.season] = run  # baad wali run pichli ko overwrite karti hai
        return latest


class CalculationRun(models.Model):
    """
    Ek calculation ki ek dafa ki chalayi (ek season, ek kind).

    Zindagi: create (status=running) -> results likho -> mark_success()
    Ghalti ho to: mark_failed(error). Fail run ke results API kabhi nahi dekhti.
    """
    kind = models.CharField(max_length=10, choices=RunKind.choices, help_text="Role ya Level.")
    season = models.SmallIntegerField(help_text="Kis season ke liye calculation.")
    spec_version = models.CharField(
        max_length=20, default=SPEC_VERSION,
        help_text="Kis spec version ke rules se bani (jaise v9.1).",
    )
    status = models.CharField(
        max_length=10, choices=RunStatus.choices, default=RunStatus.RUNNING,
        help_text="running -> success / failed.",
    )
    depends_on = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="dependents",
        help_text="Level run kis Role run ki family par chali. Role run ke liye khaali. "
                  "PROTECT: jab tak Level run us par khari hai, Role run delete nahi hogi.",
    )
    started_at = models.DateTimeField(auto_now_add=True, help_text="Run kab shuru hui.")
    finished_at = models.DateTimeField(null=True, blank=True, help_text="Run kab khatam hui (success ya fail).")
    constants_snapshot = models.JSONField(
        default=dict, blank=True,
        help_text="Is run mein istemal hue constants ki copy (audit ke liye).",
    )
    summary = models.JSONField(
        default=dict, blank=True,
        help_text="Khulasa: player counts, usage median, waghera. Validation (V-xx) mein kaam aata hai.",
    )
    error_message = models.TextField(blank=True, help_text="Fail hone par wajah.")

    objects = CalculationRunQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["kind", "season", "status"], name="calcrun_kind_season_status"),
        ]

    def clean(self):
        """
        Rishton ki jaanch. Note: Django save() par clean() khud nahi chalata;
        command mein run.full_clean() bula kar chalayein.
        """
        if self.kind == RunKind.LEVEL:
            if self.depends_on is None:
                raise ValidationError("Level run ke liye depends_on (Role run) zaroori hai.")
            if self.depends_on.kind != RunKind.ROLE:
                raise ValidationError("Level run sirf Role run par depend kar sakti hai.")
            if self.depends_on.season != self.season:
                raise ValidationError("Level aur Role run ka season ek hona chahiye.")
            if self.depends_on.status != RunStatus.SUCCESS:
                raise ValidationError("Level run sirf kamyab Role run par chal sakti hai.")
        elif self.depends_on is not None:
            raise ValidationError("Role run kisi aur run par depend nahi karti.")

    def mark_success(self, summary=None):
        """Run ko kamyab mark karo. Isi ke baad API isay dekhti hai."""
        self.status = RunStatus.SUCCESS
        self.finished_at = timezone.now()
        if summary is not None:
            self.summary = summary
        self.save(update_fields=["status", "finished_at", "summary"])

    def mark_failed(self, error):
        """Run ko fail mark karo aur wajah likho."""
        self.status = RunStatus.FAILED
        self.finished_at = timezone.now()
        self.error_message = str(error)
        self.save(update_fields=["status", "finished_at", "error_message"])

    def __str__(self):
        return f"{self.kind} {self.season} #{self.pk} ({self.status})"


# ---------------------------------------------------------------------------
# Step 1: Role
# ---------------------------------------------------------------------------

class RolePlacement(models.Model):
    """
    Ek player ka ek season ka Role natija, aur us ka audit trail.

    Teen asal outputs: primary_role, secondary_role, family.
    Baaqi fields batate hain ke faisla KYUN hua (spec 2.8 ka audit trail).
    Teammate shares (pehle alag table player_onfloor_shares) bhi yahin hain (D-11).
    """
    run = models.ForeignKey(
        CalculationRun, on_delete=models.CASCADE, related_name="placements",
        help_text="Kis Role run ka natija. Season run se aata hai (D-18).",
    )
    player = models.ForeignKey(
        Player, on_delete=models.PROTECT, related_name="role_placements",
        help_text="Kaunsa player.",
    )

    # --- Teen outputs ---
    primary_role = models.CharField(
        max_length=30, choices=Role.choices, null=True, blank=True,
        help_text="9 mein se ek archetype. NULL = data hi nahi (A-02).",
    )
    secondary_role = models.CharField(
        max_length=30, choices=Role.choices, null=True, blank=True,
        help_text="Sab se oonchi proposal jis ka role primary se alag ho. Display par 'lean'.",
    )
    family = models.CharField(
        max_length=10, choices=Family.choices, null=True, blank=True,
        help_text="Guards / Wings / Bigs, primary role se (constants.family_for_role).",
    )

    # --- Placement ki halat ---
    confidence = models.CharField(max_length=10, choices=Confidence.choices, help_text="normal ya low.")
    fallback = models.BooleanField(
        default=False,
        help_text="True = pooling ke baad bhi 300 se kam possessions; placeholder rules se (A-02).",
    )
    rules_mode = models.CharField(
        max_length=10, choices=RulesMode.choices,
        help_text="full = tagged play types (2026), coarse = purane proxies.",
    )
    history_complete = models.BooleanField(
        help_text="False = koi rule chahiye wala pichla season data mein nahi tha (D-12, L-02).",
    )
    is_qualified = models.BooleanField(
        help_text="Torvik minutes% >= 40 aur is season 300+ off. possessions. Percentiles isi population par.",
    )
    pooled_off_poss = models.IntegerField(
        null=True, blank=True,
        help_text="Pooling ke baad offensive possessions (weight ke saath).",
    )

    # --- Audit trail ---
    winning_group = models.CharField(
        max_length=20, choices=Group.choices, null=True, blank=True,
        help_text="Jis group ki proposal primary role bani.",
    )
    decided_by = models.CharField(
        max_length=30, choices=DecidedBy.choices,
        help_text="Clear top group, kaunsa tiebreaker, ya fallback.",
    )
    top3_groups = models.JSONField(
        default=list, blank=True,
        help_text='Top 3 group scores, jaise [{"group": "creation", "score": 0.88}, ...].',
    )
    top4_play_types = models.JSONField(
        default=list, blank=True,
        help_text='4 sab se oonche play-type percentiles, jaise [{"play_type": "assists", "pct": 0.85}, ...].',
    )

    # --- Teammate shares (0-1). NULL = 200 se kam valid possessions, rule skip hota hai ---
    lead = models.FloatField(null=True, blank=True, help_text="Kitne % possessions mein court par sab se bara passer tha.")
    lead2 = models.FloatField(null=True, blank=True, help_text="Kitne % mein top-2 passers mein tha.")
    inside = models.FloatField(null=True, blank=True, help_text="Kitne % mein sab se bara interior player tha (ORB+BLK+putbacks).")
    inside2 = models.FloatField(null=True, blank=True, help_text="Kitne % mein top-2 interior mein tha.")
    front = models.FloatField(null=True, blank=True, help_text="Kitne % mein 5 mein se do sab se lambon mein tha (slot 4-5).")
    shares_valid_poss = models.IntegerField(
        null=True, blank=True,
        help_text="Shares kitne possessions par gine (jahan side ke 4+ players ka read tha).",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["run", "player"], name="uniq_roleplacement_run_player"),
        ]

    @property
    def season(self):
        """Season run se (D-18). Bohot saari rows par loop karein to select_related('run') lagayein."""
        return self.run.season

    @property
    def is_close_call(self):
        """True agar faisla kisi tiebreaker ne kiya (spec: 38% placements)."""
        return self.decided_by in {
            DecidedBy.TB_CREATOR, DecidedBy.TB_INTERIOR, DecidedBy.TB_LENGTH,
            DecidedBy.TB_LARGER_SAMPLE, DecidedBy.TB_HIGHER_VOLUME,
        }

    def __str__(self):
        return f"{self.player_id} run {self.run_id}: {self.primary_role}"


class GroupScore(models.Model):
    """
    Ek player ke ek group ka score aur us group ki proposal.
    Har placement ki 7 rows (current) + 7 rows (three_season, agar sample mojood ho).
    """
    placement = models.ForeignKey(
        RolePlacement, on_delete=models.CASCADE, related_name="group_scores",
        help_text="Kis placement ka hissa.",
    )
    group = models.CharField(max_length=20, choices=Group.choices, help_text="7 groups mein se ek.")
    sample = models.CharField(
        max_length=20, choices=Sample.choices,
        help_text="current = is season (pooled); three_season = sirf tiebreaker 4 ke liye.",
    )
    raw_score = models.FloatField(
        null=True, blank=True,
        help_text="Group ke 2 sab se oonche play-type percentiles ka mean (ek ho to wahi).",
    )
    group_score = models.FloatField(
        null=True, blank=True,
        help_text="raw_score ka qualified players mein percentile (0-1). Ranking isi par.",
    )
    proposed_role = models.CharField(
        max_length=30, choices=Role.choices, null=True, blank=True,
        help_text="Is group ke rule ne kaunsa role propose kiya.",
    )
    dropped_by_guardrail = models.BooleanField(
        default=False,
        help_text="True = height guardrail ne proposal hata di (big < 6'5\" ya guard > 6'8\").",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["placement", "group", "sample"], name="uniq_groupscore_placement_group_sample"
            ),
        ]

    def __str__(self):
        return f"{self.placement_id} {self.group}/{self.sample}: {self.group_score}"


# ---------------------------------------------------------------------------
# Step 2: Level
# ---------------------------------------------------------------------------

class SeasonLevelValues(models.Model):
    """
    Ek Level run ke season-wide numbers. Validation V-10 se V-17 inhi se match hote hain.
    """
    run = models.OneToOneField(
        CalculationRun, on_delete=models.CASCADE, related_name="level_values",
        help_text="Kis Level run ke numbers.",
    )

    # --- Event prices ---
    league_ft_pct = models.FloatField(help_text="League FT% (2026 spec: .7223).")
    league_ppp = models.FloatField(
        null=True, blank=True,
        help_text="League ke asal points per possession. Sirf context; kisi price mein nahi (PPP fixed 1.075).",
    )
    xpts_rim = models.FloatField(help_text="Rim shot ki expected value (2026 spec: 1.3100).")
    xpts_mid = models.FloatField(help_text="Mid-range shot ki expected value (2026 spec: 0.9548).")
    xpts_three = models.FloatField(help_text="Three ki expected value (2026 spec: 1.2139).")
    ast_share_jumper = models.FloatField(help_text="National assisted share, mid + three mila kar.")

    # --- Points per win (scoreboard regression) ---
    d1_teams = models.IntegerField(help_text="Is season D1 teams.")
    ppw_teams = models.IntegerField(help_text="Regression mein teams (D1, 10+ games).")
    ppw_intercept = models.FloatField(help_text="y = a + b*x ka a.")
    ppw_slope = models.FloatField(help_text="y = a + b*x ka b.")
    ppw_r = models.FloatField(help_text="Correlation r.")
    points_per_win = models.FloatField(help_text="1 / slope. Kitne extra points = 1 extra jeet (2026 spec: 41.69).")

    # --- Replacement level (EPA/40) ---
    bench_players = models.IntegerField(help_text="Bench band mein players (D1, 50-149 minutes).")
    replacement_all = models.FloatField(help_text="Overall bench EPA/40 (family nahi to yahi).")
    replacement_guards = models.FloatField(help_text="Guards ka replacement.")
    replacement_wings = models.FloatField(help_text="Wings ka replacement.")
    replacement_bigs = models.FloatField(help_text="Bigs ka replacement.")

    class Meta:
        verbose_name_plural = "season level values"

    def replacement_for(self, family):
        """Family ke hisaab se replacement. None ya khaali family = overall."""
        return {
            Family.GUARDS: self.replacement_guards,
            Family.WINGS: self.replacement_wings,
            Family.BIGS: self.replacement_bigs,
        }.get(family, self.replacement_all)

    def __str__(self):
        return f"Level values run {self.run_id}"


class PlayerSeasonLevel(models.Model):
    """
    Ek player ka ek season ka Level natija: 11 EPA pieces se tier tak.

    Pieces SEASON TOTALS hain (per 40 nahi). Per 40 chahiye to pieces_per40().
    """
    run = models.ForeignKey(
        CalculationRun, on_delete=models.CASCADE, related_name="levels",
        help_text="Kis Level run ka natija.",
    )
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="levels", help_text="Kaunsa player.")
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="+", help_text="Is season player ki team.")
    role_placement = models.ForeignKey(
        RolePlacement, on_delete=models.PROTECT, null=True, blank=True, related_name="levels",
        help_text="Family kis Role placement se aayi (D-16). NULL = Role data nahi tha.",
    )
    family = models.CharField(
        max_length=10, choices=Family.choices, null=True, blank=True,
        help_text="Is calculation ne kaunsi family istemal ki. NULL = overall replacement laga.",
    )
    minutes = models.IntegerField(help_text="Regular-season minutes (box).")
    coverage = models.FloatField(
        null=True, blank=True,
        help_text="pbp points / box points. 0.80 se kam = not rated.",
    )

    # --- 11 pieces (season totals, points mein) ---
    epa_self_creation = models.FloatField(help_text="Apna banaya shot.")
    epa_shooting = models.FloatField(help_text="Catch-and-shoot jumpers.")
    epa_finishing = models.FloatField(help_text="Assisted rim finishes (cuts, rolls, lobs).")
    epa_ft_drawing = models.FloatField(help_text="Free throw line tak pohanchna.")
    epa_ft_making = models.FloatField(help_text="Free throws league rate se behtar / badtar daalna.")
    epa_creation = models.FloatField(help_text="Assists se doosron ke liye value.")
    epa_ball_security = models.FloatField(help_text="Turnovers (hamesha negative ya 0).")
    epa_off_rebounds = models.FloatField(help_text="Offensive rebounds (A-04: 0.785 each).")
    epa_steals = models.FloatField(help_text="Steals (1.075 each).")
    epa_blocks = models.FloatField(help_text="Blocks (0.750 each).")
    epa_discipline = models.FloatField(help_text="Fouls aur technicals (negative ya 0).")
    epa_total = models.FloatField(help_text="11 pieces ka jama.")

    # --- Total se tier tak ---
    epa_per40 = models.FloatField(null=True, blank=True, help_text="EPA / minutes * 40.")
    surplus_per40 = models.FloatField(null=True, blank=True, help_text="EPA/40 - replacement.")
    war_per40 = models.FloatField(null=True, blank=True, help_text="surplus/40 / points per win. Quality; tier isi par.")
    war = models.FloatField(null=True, blank=True, help_text="war_per40 * minutes/40 * min(1, minutes/400).")
    tier = models.CharField(
        max_length=20, choices=Tier.choices, null=True, blank=True,
        help_text="WAR per 40 se rang. NULL = not rated.",
    )

    # --- Flags ---
    is_d1 = models.BooleanField(help_text="Player ki team is season D1 thi.")
    is_rated = models.BooleanField(help_text="coverage >= 0.80.")
    is_qualified = models.BooleanField(help_text="400+ minutes, rated, D1 (tier bars wali population).")
    history_complete = models.BooleanField(help_text="False = replacement ke liye pas-pados ka season data mein nahi tha.")

    PIECE_FIELDS = (
        "epa_self_creation", "epa_shooting", "epa_finishing", "epa_ft_drawing",
        "epa_ft_making", "epa_creation", "epa_ball_security", "epa_off_rebounds",
        "epa_steals", "epa_blocks", "epa_discipline",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["run", "player"], name="uniq_playerseasonlevel_run_player"),
        ]

    def pieces(self):
        """11 pieces ek dict mein: {"epa_self_creation": 12.3, ...}."""
        return {name: getattr(self, name) for name in self.PIECE_FIELDS}

    def pieces_per40(self):
        """11 pieces per 40 minutes. Minutes 0 ho to None (divide by zero se bachao)."""
        if not self.minutes:
            return None
        return {name: value / self.minutes * 40 for name, value in self.pieces().items()}

    def pieces_add_up(self, tolerance=1e-6):
        """Spec: pieces wapas total ke barabar jama hone chahiyein. Validation check."""
        return abs(sum(self.pieces().values()) - self.epa_total) <= tolerance

    @property
    def season(self):
        """Season run se (D-18)."""
        return self.run.season

    def __str__(self):
        return f"{self.player_id} run {self.run_id}: {self.tier}"