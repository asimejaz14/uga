"""
Database <-> pandas.

Reading:  each load_* function returns a DataFrame whose columns match the model's
          database columns (FKs appear as player_id / game_id = the external IDs).
Writing:  each save_* function replaces the rows for the given seasons, inside one
          transaction, so re-running a step never leaves duplicates or half-written data.

No calculation happens here. If you are looking for a formula, it is in the step modules.
"""
from decimal import Decimal

import pandas as pd
from django.db import transaction

from ..models import (
    Game, ModelConstant, NationalAssistShare, PlayerSeasonCounts, PlayerSeasonPossessions,
    PlayerGroupScore, PlayerOnfloorShares, Possession, RolePlacement, TorvikPlayerSeason,
)

BATCH = 5000

POSSESSION_COLS = [
    "game_id", "possession_no", "season", "off_team_id", "def_team_id",
    "off_p1", "off_p2", "off_p3", "off_p4", "off_p5",
    "def_p1", "def_p2", "def_p3", "def_p4", "def_p5",
    "garbage_time",
]
GAME_COLS = ["game_id", "season", "season_type", "tournament_id", "has_shot_tags"]


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------

def _frame(queryset, columns):
    """Turn a queryset into a DataFrame with exactly these columns (even when empty)."""
    rows = list(queryset.values_list(*columns))
    return pd.DataFrame(rows, columns=columns)


def all_seasons():
    """Every season that has games, oldest first."""
    return sorted(Game.objects.values_list("season", flat=True).distinct())


def load_games(seasons):
    return _frame(Game.objects.filter(season__in=seasons), GAME_COLS)


def load_possessions(seasons):
    # Player columns can be NULL in real data, so read them as nullable integers.
    df = _frame(Possession.objects.filter(season__in=seasons), POSSESSION_COLS)
    player_cols = [c for c in POSSESSION_COLS if c[-3:-1] == "_p"]
    return df.astype({c: "Int64" for c in player_cols})


def load_counts(seasons):
    """PlayerSeasonCounts for these seasons, all columns except Django's surrogate id."""
    cols = [f.attname for f in PlayerSeasonCounts._meta.concrete_fields if f.attname != "id"]
    return _frame(PlayerSeasonCounts.objects.filter(season__in=seasons), cols)


def load_player_possessions(seasons):
    """PlayerSeasonPossessions (Step 1 output). tagged_off_poss is NaN before 2026."""
    cols = ["player_id", "season", "team_id", "off_poss", "def_poss", "tagged_off_poss"]
    df = _frame(PlayerSeasonPossessions.objects.filter(season__in=seasons), cols)
    df["tagged_off_poss"] = pd.to_numeric(df["tagged_off_poss"], errors="coerce")
    return df


def load_torvik(seasons):
    """Torvik attributes as floats (the model stores Decimals). Missing height -> NaN."""
    cols = ["player_id", "season", "team_id", "height_in", "min_pct", "usage", "three_pa_share"]
    df = _frame(TorvikPlayerSeason.objects.filter(season__in=seasons), cols)
    for c in ["height_in", "min_pct", "usage", "three_pa_share"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def load_national_share(season):
    """NationalAssistShare (Step 2 output) for one season as {"rim": .., "mid": .., "three": ..}."""
    rows = NationalAssistShare.objects.filter(season=season).values_list("zone", "ast_share")
    share = {zone: float(v) for zone, v in rows}
    missing = {"rim", "mid", "three"} - set(share)
    if missing:
        raise ValueError(f"NationalAssistShare missing {sorted(missing)} for {season}: "
                         "run the assist_share step first")
    return share


def load_constants(spec_version="9.1"):
    """model_constants as {key: float}. Raises if the table is empty."""
    c = {k: float(v) for k, v in ModelConstant.as_dict(spec_version).items()}
    if not c:
        raise ValueError(f"no model_constants for spec {spec_version}: run seed_role_dummy")
    return c


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

@transaction.atomic
def save_player_season_possessions(df, seasons):
    """Replace PlayerSeasonPossessions for `seasons` with the rows in df."""
    PlayerSeasonPossessions.objects.filter(season__in=seasons).delete()
    objs = [
        PlayerSeasonPossessions(
            player_id=int(r.player_id),          # external player ID (FK to_field)
            season=int(r.season),
            team_id=int(r.team_id),
            off_poss=int(r.off_poss),
            def_poss=int(r.def_poss),
            tagged_off_poss=None if pd.isna(r.tagged_off_poss) else int(r.tagged_off_poss),
        )
        for r in df.itertuples(index=False)
    ]
    PlayerSeasonPossessions.objects.bulk_create(objs, batch_size=BATCH)
    return len(objs)


@transaction.atomic
def save_national_assist_share(df, seasons):
    """Replace NationalAssistShare for `seasons` with the rows in df."""
    NationalAssistShare.objects.filter(season__in=seasons).delete()
    objs = [
        NationalAssistShare(
            season=int(r.season),
            zone=r.zone,
            # the column holds 4 decimal places; round explicitly so nothing is lost silently
            ast_share=Decimal(str(round(float(r.ast_share), 4))),
        )
        for r in df.itertuples(index=False)
    ]
    NationalAssistShare.objects.bulk_create(objs, batch_size=BATCH)
    return len(objs)


def _dec4(v):
    """Share (0-1) -> Decimal with 4 places, or None when the share is missing."""
    return None if pd.isna(v) else Decimal(str(round(float(v), 4)))


@transaction.atomic
def save_onfloor_shares(df, seasons):
    """Replace PlayerOnfloorShares for `seasons` with the rows in df.
    (front_poss is only in the CSV dump; the model has no column for it.)"""
    PlayerOnfloorShares.objects.filter(season__in=seasons).delete()
    objs = [
        PlayerOnfloorShares(
            player_id=int(r.player_id),
            season=int(r.season),
            valid_poss=int(r.valid_poss),
            lead=_dec4(r.lead), lead2=_dec4(r.lead2),
            inside=_dec4(r.inside), inside2=_dec4(r.inside2),
            front=_dec4(r.front),
        )
        for r in df.itertuples(index=False)
    ]
    PlayerOnfloorShares.objects.bulk_create(objs, batch_size=BATCH)
    return len(objs)


@transaction.atomic
def save_group_scores(rows, seasons):
    """Replace PlayerGroupScore for `seasons`.
    rows: DataFrame with player_id, season, group_name, sample, raw_score, group_score,
          proposed_role (None for the three-season sample)."""
    PlayerGroupScore.objects.filter(season__in=seasons).delete()
    objs = [
        PlayerGroupScore(
            player_id=int(r.player_id), season=int(r.season),
            group_name=r.group_name, sample=r.sample,
            raw_score=_dec4(r.raw_score), group_score=_dec4(r.group_score),
            proposed_role=None if pd.isna(r.proposed_role) else r.proposed_role,
        )
        for r in rows.itertuples(index=False)
    ]
    PlayerGroupScore.objects.bulk_create(objs, batch_size=BATCH)
    return len(objs)


@transaction.atomic
def save_role_placements(df, seasons, spec_version="9.1"):
    """Replace RolePlacement for `seasons` and this spec version."""
    RolePlacement.objects.filter(season__in=seasons, spec_version=spec_version).delete()
    objs = [
        RolePlacement(
            player_id=int(r.player_id), season=int(r.season),
            primary_role=r.primary_role, secondary_role=r.secondary_role,
            family=r.family, confidence=r.confidence, fallback=bool(r.fallback),
            rules_mode=r.rules_mode, pooled_off_poss=int(r.pooled_off_poss),
            winning_group=r.winning_group, top3_groups=r.top3_groups,
            decided_by=r.decided_by, top4_play_types=r.top4_play_types,
            lead=_dec4(r.lead), inside=_dec4(r.inside), spec_version=spec_version,
        )
        for r in df.itertuples(index=False)
    ]
    RolePlacement.objects.bulk_create(objs, batch_size=BATCH)
    return len(objs)
