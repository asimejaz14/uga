"""
Step 3 — who is qualified, and how many seasons a player's counts are pooled over.

Spec (v9.1, section 2.3, "Who is in the population" and "What a season means here"):

  Qualified   Torvik minutes % >= 40  AND  300+ offensive possessions THIS season
              -> the reference population for every percentile later on

  Placement reads possessions, not seasons:
    Established   (300+ offensive possessions this season)
                  counts = this season + 0.5 x last season          confidence = normal
    Low-minute    (under 300 this season)
                  counts = this season + 1.0 x last season
                  still under 300 -> also + 1.0 x the season before   confidence = low
    Still < 300   no read -> fallback = True (matrix fit, not the rules)   confidence = low

  "Counts add, then rates are made from the pooled counts."
      So we pool the COUNTS and the POSSESSIONS with the same weights, and Step 4
      divides one by the other. We never average rates.

  2026 shot tags are 2026 only and never pooled: tagged columns and tagged_off_poss
  are taken from the target season as they are.

  Three-season sample (tiebreaker 4 only): this + last + the one before, all at full
  weight, 300+ required. Built here with the same machinery, used in a later step.

Output of pool_season(): one row per player who was on the floor in the target season:
    player_id, season, team_id,
    off_poss_this                      (this season, unpooled — the qualified gate uses it)
    off_poss, def_poss                 (pooled)
    <every count column>               (pooled; tagged columns = target season only)
    tagged_off_poss                    (target season only)
    qualified, read, fallback, confidence, seasons_used
"""
import numpy as np
import pandas as pd

# Count columns that exist every season and are pooled.
POOLED_COUNTS = [
    "assists", "ast_to_three", "ast_to_rim", "ft_trips", "transition_fga",
    "steals", "blocks", "drb", "orb", "putbacks",
    "fga_rim", "fgm_rim", "fgm_rim_ast",
    "fga_mid", "fgm_mid", "fgm_mid_ast",
    "fga_three", "fgm_three", "fgm_three_ast",
]
# 2026 tagged columns: taken from the target season only, never pooled.
TAGGED_COUNTS = [
    "driving_layups", "pullups_2", "pullup_range_2s", "floaters", "pullups_3",
    "plain_rim_fga", "plain_rim_fgm", "plain_rim_fgm_ast",
    "tip_ins", "hooks_turnarounds", "alley_oops",
]
POOLED = ["off_poss", "def_poss"] + POOLED_COUNTS


def _season_block(poss, counts, season):
    """Possessions + counts for one season, indexed by player_id, pooled columns only.
    A player missing from that season simply isn't in the index (treated as 0 later)."""
    p = poss[poss["season"] == season].set_index("player_id")[["off_poss", "def_poss"]]
    c = counts[counts["season"] == season].set_index("player_id")[POOLED_COUNTS]
    return p.join(c, how="left").fillna(0).astype(float)


def qualified_mask(off_poss_this, min_pct, c):
    """Qualified = Torvik minutes % >= 40 AND 300+ offensive possessions this season.
    A player with no Torvik row has min_pct NaN and is therefore not qualified."""
    return (min_pct >= c["MIN_PCT_QUALIFIED"]) & (off_poss_this >= c["MIN_POSS"])


def pool_season(poss, counts, torvik, season, c):
    """Main entry point for Step 3 (the placement sample).

    poss    PlayerSeasonPossessions rows for season, season-1, season-2
    counts  PlayerSeasonCounts rows for the same seasons
    torvik  TorvikPlayerSeason rows for `season`
    c       constants dict (MIN_POSS, MIN_PCT_QUALIFIED, PREV_SEASON_WEIGHT)
    """
    this = _season_block(poss, counts, season)
    prev1 = _season_block(poss, counts, season - 1).reindex(this.index, fill_value=0)
    prev2 = _season_block(poss, counts, season - 2).reindex(this.index, fill_value=0)
    min_poss = c["MIN_POSS"]

    established = this["off_poss"] >= min_poss

    # Established: + half of last season.  Low-minute: + all of last season.
    w_prev = np.where(established, c["PREV_SEASON_WEIGHT"], 1.0)
    pooled = this + prev1.mul(w_prev, axis=0)

    # Low-minute and still short: add the season before at full weight.
    needs_more = ~established & (pooled["off_poss"] < min_poss)
    pooled.loc[needs_more] += prev2.loc[needs_more]

    out = pooled.copy()
    out["off_poss_this"] = this["off_poss"]
    out["read"] = out["off_poss"] >= min_poss
    out["fallback"] = ~out["read"]
    out["confidence"] = np.where(established, "normal", "low")
    out["seasons_used"] = _seasons_used(season, established, needs_more, prev1, prev2)

    return _finish(out, poss, counts, torvik, season, c)


def pool_three_season(poss, counts, torvik, season, c):
    """The three-season sample for tiebreaker 4: all three seasons at full weight.
    `read` says whether it reaches 300 offensive possessions."""
    this = _season_block(poss, counts, season)
    prev1 = _season_block(poss, counts, season - 1).reindex(this.index, fill_value=0)
    prev2 = _season_block(poss, counts, season - 2).reindex(this.index, fill_value=0)
    out = this + prev1 + prev2
    out["off_poss_this"] = this["off_poss"]
    out["read"] = out["off_poss"] >= c["MIN_POSS"]
    out["fallback"] = ~out["read"]
    out["confidence"] = "n/a"
    out["seasons_used"] = f"{season - 2}-{season}"
    return _finish(out, poss, counts, torvik, season, c)


def _seasons_used(season, established, needs_more, prev1, prev2):
    """Human-readable audit text, e.g. '2026+0.5x2025' or '2026+2025+2024'."""
    had1 = prev1["off_poss"] > 0
    had2 = prev2["off_poss"] > 0
    txt = pd.Series(str(season), index=established.index)
    txt[established & had1] += f"+0.5x{season - 1}"
    txt[~established & had1] += f"+{season - 1}"
    txt[needs_more & had2] += f"+{season - 2}"
    return txt


def _finish(out, poss, counts, torvik, season, c):
    """Add the unpooled pieces (team, tagged columns, Torvik) and the qualified flag."""
    cur_poss = poss[poss["season"] == season].set_index("player_id")
    cur_counts = counts[counts["season"] == season].set_index("player_id")
    tv = torvik[torvik["season"] == season].set_index("player_id")

    out["season"] = season
    out["team_id"] = cur_poss["team_id"]
    # never pooled; NULL (pre-2026) becomes NaN
    out["tagged_off_poss"] = pd.to_numeric(cur_poss["tagged_off_poss"], errors="coerce")
    for col in TAGGED_COUNTS:
        out[col] = pd.to_numeric(cur_counts[col], errors="coerce") if col in cur_counts else np.nan

    # Torvik attributes travel with the row; later steps (rules) need them.
    for col in ["height_in", "min_pct", "usage", "three_pa_share"]:
        out[col] = pd.to_numeric(tv[col], errors="coerce") if col in tv else np.nan

    out["qualified"] = qualified_mask(out["off_poss_this"], out["min_pct"], c)
    out.index.name = "player_id"
    return out.reset_index()
