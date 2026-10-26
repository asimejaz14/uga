"""
Django models for the Role (Step 1) schema — spec v9.1.

App-ready version:
  * Django owns the schema (managed=True) — create tables with migrations,
    not schema.sql.
  * Every table has a surrogate `id` (DEFAULT_AUTO_FIELD = BigAutoField); the
    old composite primary keys are now UniqueConstraints.
  * players.player_id and games.game_id are unique external IDs, and every
    ForeignKey points at them (to_field), so the player_id / game_id columns
    in other tables hold the real external IDs, not Django's surrogate id.

Requires Django 5.1+.
Tables go into the Postgres schema `role` via the search path:
    DATABASES["default"]["OPTIONS"] = {"options": "-c search_path=role,public"}
"""
from django.db import models
from django.db.models import Q, F
from django.db.models.functions import Now


# ---------------------------------------------------------------------
# Choices
# ---------------------------------------------------------------------

class Zone(models.TextChoices):
    RIM = "rim"
    MID = "mid"
    THREE = "three"


class GroupName(models.TextChoices):
    CREATION = "creation"
    SELF_CREATION = "self_creation"
    SHOOTING = "shooting"
    STEALS = "steals"
    DEF_GLASS = "def_glass"
    BLOCKS = "blocks"
    INSIDE = "inside"


class Sample(models.TextChoices):
    CURRENT = "current"
    THREE_SEASON = "three_season"


class Family(models.TextChoices):
    GUARDS = "Guards"
    WINGS = "Wings"
    BIGS = "Bigs"


class Confidence(models.TextChoices):
    NORMAL = "normal"
    LOW = "low"


class RulesMode(models.TextChoices):
    FULL = "full"
    COARSE = "coarse"


class DecidedBy(models.TextChoices):
    CLEAR = "clear"
    CREATOR = "creator"
    INTERIOR = "interior"
    LENGTH = "length"
    LARGER_SAMPLE = "larger_sample"
    VOLUME = "volume"
    FALLBACK = "fallback"


# ---------------------------------------------------------------------
# 1. REFERENCE
# ---------------------------------------------------------------------

class Team(models.Model):
    """One row per team per season. `team_id` is the external team ID."""
    team_id = models.IntegerField()
    season = models.SmallIntegerField()
    team_name = models.TextField()
    conference_id = models.IntegerField(null=True, blank=True)  # NULL = not D1 that season

    class Meta:
        db_table = "teams"
        constraints = [
            models.UniqueConstraint(fields=["team_id", "season"], name="teams_team_season_uniq"),
        ]

    def __str__(self):
        return f"{self.team_name} ({self.season})"


class Player(models.Model):
    player_id = models.IntegerField(unique=True)   # external ID
    player_name = models.TextField()

    class Meta:
        db_table = "players"

    def __str__(self):
        return self.player_name


class Game(models.Model):
    game_id = models.BigIntegerField(unique=True)  # external ID
    season = models.SmallIntegerField()
    game_date = models.DateField()
    # External team IDs. Look up the Team row with (team_id, season).
    home_team_id = models.IntegerField()
    away_team_id = models.IntegerField()
    season_type = models.SmallIntegerField()                      # 2 = regular season
    tournament_id = models.IntegerField(null=True, blank=True)     # NOT NULL = excluded
    has_shot_tags = models.BooleanField(default=False)

    class Meta:
        db_table = "games"
        indexes = [models.Index(fields=["season"], name="games_season_idx")]


# ---------------------------------------------------------------------
# 2. RAW INPUTS
# ---------------------------------------------------------------------

class Possession(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, to_field="game_id",
                             related_name="possessions")
    possession_no = models.IntegerField()
    season = models.SmallIntegerField()
    off_team_id = models.IntegerField()
    def_team_id = models.IntegerField()

    # On-floor fives: kept as plain player IDs (10 FKs on the biggest table
    # would slow bulk loads and add 10 indexes).
    off_p1 = models.IntegerField(null=True, blank=True)
    off_p2 = models.IntegerField(null=True, blank=True)
    off_p3 = models.IntegerField(null=True, blank=True)
    off_p4 = models.IntegerField(null=True, blank=True)
    off_p5 = models.IntegerField(null=True, blank=True)
    def_p1 = models.IntegerField(null=True, blank=True)
    def_p2 = models.IntegerField(null=True, blank=True)
    def_p3 = models.IntegerField(null=True, blank=True)
    def_p4 = models.IntegerField(null=True, blank=True)
    def_p5 = models.IntegerField(null=True, blank=True)

    garbage_time = models.BooleanField(default=False)

    class Meta:
        db_table = "possessions"
        constraints = [
            models.UniqueConstraint(fields=["game", "possession_no"], name="poss_game_no_uniq"),
        ]
        indexes = [models.Index(fields=["season"], name="poss_season_idx")]


class PlayerSeasonCounts(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="season_counts")
    season = models.SmallIntegerField()
    team_id = models.IntegerField()

    # available every season
    assists = models.IntegerField()
    ast_to_three = models.IntegerField()
    ast_to_rim = models.IntegerField()
    ft_trips = models.IntegerField()
    transition_fga = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    drb = models.IntegerField()
    orb = models.IntegerField()
    putbacks = models.IntegerField()

    # shots by zone
    fga_rim = models.IntegerField()
    fgm_rim = models.IntegerField()
    fgm_rim_ast = models.IntegerField()
    fga_mid = models.IntegerField()
    fgm_mid = models.IntegerField()
    fgm_mid_ast = models.IntegerField()
    fga_three = models.IntegerField()
    fgm_three = models.IntegerField()
    fgm_three_ast = models.IntegerField()

    # 2026 tagged play types (NULL before 2026)
    driving_layups = models.IntegerField(null=True, blank=True)
    pullups_2 = models.IntegerField(null=True, blank=True)
    pullup_range_2s = models.IntegerField(null=True, blank=True)
    floaters = models.IntegerField(null=True, blank=True)
    pullups_3 = models.IntegerField(null=True, blank=True)
    plain_rim_fga = models.IntegerField(null=True, blank=True)
    plain_rim_fgm = models.IntegerField(null=True, blank=True)
    plain_rim_fgm_ast = models.IntegerField(null=True, blank=True)
    tip_ins = models.IntegerField(null=True, blank=True)
    hooks_turnarounds = models.IntegerField(null=True, blank=True)
    alley_oops = models.IntegerField(null=True, blank=True)  # stored, in no group yet

    class Meta:
        db_table = "player_season_counts"
        constraints = [
            models.UniqueConstraint(fields=["player", "season"], name="psc_player_season_uniq"),
            models.CheckConstraint(
                condition=Q(fgm_rim__lte=F("fga_rim")) & Q(fgm_rim_ast__lte=F("fgm_rim")),
                name="psc_rim_makes_valid"),
            models.CheckConstraint(
                condition=Q(fgm_mid__lte=F("fga_mid")) & Q(fgm_mid_ast__lte=F("fgm_mid")),
                name="psc_mid_makes_valid"),
            models.CheckConstraint(
                condition=Q(fgm_three__lte=F("fga_three")) & Q(fgm_three_ast__lte=F("fgm_three")),
                name="psc_three_makes_valid"),
            models.CheckConstraint(
                condition=Q(assists__gte=F("ast_to_three") + F("ast_to_rim")),
                name="psc_assist_split_valid"),
            models.CheckConstraint(
                condition=Q(putbacks__lte=F("fga_rim")),
                name="psc_putbacks_valid"),
        ]


class TorvikPlayerSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="torvik_seasons")
    season = models.SmallIntegerField()
    team_id = models.IntegerField()
    height_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    min_pct = models.DecimalField(max_digits=5, decimal_places=2)
    usage = models.DecimalField(max_digits=5, decimal_places=2)
    three_pa_share = models.DecimalField(max_digits=5, decimal_places=4)  # 0–1

    class Meta:
        db_table = "torvik_player_season"
        constraints = [
            models.UniqueConstraint(fields=["player", "season"], name="torvik_player_season_uniq"),
        ]


# ---------------------------------------------------------------------
# 3. DERIVED
# ---------------------------------------------------------------------

class PlayerSeasonPossessions(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="season_possessions")
    season = models.SmallIntegerField()
    team_id = models.IntegerField()
    off_poss = models.IntegerField()
    def_poss = models.IntegerField()
    tagged_off_poss = models.IntegerField(null=True, blank=True)  # 2026 only

    class Meta:
        db_table = "player_season_possessions"
        constraints = [
            models.UniqueConstraint(fields=["player", "season"], name="psp_player_season_uniq"),
        ]


class NationalAssistShare(models.Model):

    season = models.SmallIntegerField()
    zone = models.TextField(choices=Zone.choices)
    ast_share = models.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        db_table = "national_assist_share"
        constraints = [
            models.UniqueConstraint(fields=["season", "zone"], name="nas_season_zone_uniq"),
            models.CheckConstraint(condition=Q(zone__in=Zone.values), name="nas_zone_valid"),
        ]


# ---------------------------------------------------------------------
# 4. CONFIG
# ---------------------------------------------------------------------

class ModelConstant(models.Model):

    spec_version = models.TextField()
    key = models.TextField()
    value = models.DecimalField(max_digits=20, decimal_places=6)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "model_constants"
        constraints = [
            models.UniqueConstraint(fields=["spec_version", "key"], name="mc_version_key_uniq"),
        ]

    def __str__(self):
        return f"{self.spec_version} {self.key} = {self.value}"

    @classmethod
    def as_dict(cls, spec_version="9.1"):
        return dict(cls.objects.filter(spec_version=spec_version).values_list("key", "value"))


# ---------------------------------------------------------------------
# 5. OUTPUTS
# ---------------------------------------------------------------------

class PlayerOnfloorShares(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="onfloor_shares")
    season = models.SmallIntegerField()
    valid_poss = models.IntegerField()  # possessions with 4+ reads on his side
    lead = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    lead2 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    inside = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    inside2 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    front = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = "player_onfloor_shares"
        constraints = [
            models.UniqueConstraint(fields=["player", "season"], name="pos_player_season_uniq"),
        ]


class PlayerGroupScore(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="group_scores")
    season = models.SmallIntegerField()
    group_name = models.TextField(choices=GroupName.choices)
    sample = models.TextField(choices=Sample.choices, default=Sample.CURRENT)
    raw_score = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    group_score = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    proposed_role = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "player_group_scores"
        constraints = [
            models.UniqueConstraint(fields=["player", "season", "group_name", "sample"],
                                    name="pgs_player_season_group_sample_uniq"),
            models.CheckConstraint(condition=Q(group_name__in=GroupName.values), name="pgs_group_valid"),
            models.CheckConstraint(condition=Q(sample__in=Sample.values), name="pgs_sample_valid"),
        ]


class RolePlacement(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="role_placements")
    season = models.SmallIntegerField()
    primary_role = models.TextField()
    secondary_role = models.TextField(null=True, blank=True)
    family = models.TextField(choices=Family.choices)
    confidence = models.TextField(choices=Confidence.choices)
    fallback = models.BooleanField(default=False)
    rules_mode = models.TextField(choices=RulesMode.choices)
    pooled_off_poss = models.IntegerField(null=True, blank=True)
    winning_group = models.TextField(null=True, blank=True)
    top3_groups = models.JSONField(null=True, blank=True)      # [{"group","score","role"}, ...]
    decided_by = models.TextField(choices=DecidedBy.choices, null=True, blank=True)
    top4_play_types = models.JSONField(null=True, blank=True)  # [{"play_type","pctl"}, ...]
    lead = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    inside = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    spec_version = models.TextField(default="9.1")
    computed_at = models.DateTimeField(db_default=Now())

    class Meta:
        db_table = "role_placement"
        constraints = [
            models.UniqueConstraint(fields=["player", "season", "spec_version"],
                                    name="rp_player_season_version_uniq"),
            models.CheckConstraint(condition=Q(family__in=Family.values), name="rp_family_valid"),
            models.CheckConstraint(condition=Q(confidence__in=Confidence.values), name="rp_confidence_valid"),
            models.CheckConstraint(condition=Q(rules_mode__in=RulesMode.values), name="rp_rules_mode_valid"),
        ]


# ---------------------------------------------------------------------
# 6. DUMMY ONLY — drop for real data
# ---------------------------------------------------------------------

class DummyTruth(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field="player_id",
                               related_name="dummy_truths")
    season = models.SmallIntegerField()
    archetype = models.TextField()

    class Meta:
        db_table = "dummy_truth"
        constraints = [
            models.UniqueConstraint(fields=["player", "season"], name="dt_player_season_uniq"),
        ]