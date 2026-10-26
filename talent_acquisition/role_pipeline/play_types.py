"""
Step 4 — play types, rates per 100, and percentiles.

Three conversions, in this order (spec 2.4 and 2.5):

  1. COUNTS -> PLAY TYPES
     Most play types are a count as it is (assists, steals ...). A few are built from
     the assisted share of his makes, shrunk toward the national share over 5 makes:
         a = (assisted makes + 5 x national share) / (makes + 5)

         own threes            = 3PA x (1 - a_three)
         catch-and-shoot 3s    = 3PA x a_three
         catch-and-shoot mid   = mid 2PA x a_mid

     2015-2025 (coarse rules) add three proxies for the 2026 tags:
         unassisted rim  = (rim FGA - putbacks) x (1 - a_rim)    stands in for driving layups
         unassisted mid  = mid 2PA x (1 - a_mid)                  stands in for pull-ups
         assisted rim    = (rim FGA - putbacks) x a_rim           stands in for cut/roll

     2026 (full rules) add eight tagged play types instead:
         driving layups, pull-ups & step-backs, pull-up range 2s, floaters,
         three-point pull-ups, cut & roll (= plain rim FGA x a_plain_rim),
         tip-ins, hooks & turnarounds.        Alley-oops are stored but used nowhere.

     2015-2025: 13 base + 3 coarse = 16 play types
     2026:      13 base + 8 tagged = 21 play types

  2. PLAY TYPE -> RATE PER 100
         rate = count / possessions x 100
     offence   per 100 OFFENSIVE possessions (pooled)
     defence   per 100 DEFENSIVE possessions (pooled): steals, blocks, defensive rebounds
     tagged    per 100 offensive possessions IN TAGGED GAMES (2026 only, unpooled);
               no tagged games -> blank, and the play type is skipped later
     pull-up range 2s: full 2026 season (shot locations exist in every 2026 game),
               so per 100 of his 2026 offensive possessions

  3. RATE -> PERCENTILE (0 to 1)
         percentile = share of QUALIFIED players this season with a LOWER rate
     Every player (qualified or not) is placed against the qualified distribution.
     Example: 100 qualified players, 85 have a lower assist rate -> 0.85
"""
import numpy as np
import pandas as pd

from .assist_share import shrunk_assisted_share

BASE = ["assists", "ast_to_three", "ast_to_rim", "ft_trips", "transition",
        "own_threes", "cs_threes", "cs_mid",
        "steals", "blocks", "drb", "orb", "putbacks"]
COARSE = ["unassisted_rim", "unassisted_mid", "assisted_rim"]
TAGGED = ["driving_layups", "pullups_2", "pullup_range_2s", "floaters", "pullups_3",
          "cut_roll", "tip_ins", "hooks_turnarounds"]

DEFENSIVE = {"steals", "blocks", "drb"}            # per 100 defensive possessions
FULL_SEASON_TAGGED = {"pullup_range_2s"}           # per 100 of his 2026 off. possessions


def play_types_for(mode):
    """The play types that enter the groups for a rules mode ('full' or 'coarse')."""
    return BASE + (TAGGED if mode == "full" else COARSE)


def rules_mode(season, games):
    """'full' when the season has shot-tagged games (2026), otherwise 'coarse'."""
    tagged_seasons = set(games.loc[games["has_shot_tags"].astype(bool), "season"])
    return "full" if season in tagged_seasons else "coarse"


# ---------------------------------------------------------------------------
# 1. counts -> play types
# ---------------------------------------------------------------------------

def build_play_types(pooled, national, mode, k=5):
    """Play-type COUNTS per player.

    pooled    output of pooling.pool_season (one row per player)
    national  dict zone -> national assisted share for this season, e.g. {"rim": 0.49, ...}
    mode      'full' or 'coarse'
    k         shrink strength (SHRINK_K = 5)
    """
    p = pooled
    a_rim = shrunk_assisted_share(p["fgm_rim_ast"], p["fgm_rim"], national["rim"], k)
    a_mid = shrunk_assisted_share(p["fgm_mid_ast"], p["fgm_mid"], national["mid"], k)
    a_three = shrunk_assisted_share(p["fgm_three_ast"], p["fgm_three"], national["three"], k)

    pt = pd.DataFrame(index=p.index)
    # --- 13 base play types (every season) ---
    pt["assists"] = p["assists"]
    pt["ast_to_three"] = p["ast_to_three"]
    pt["ast_to_rim"] = p["ast_to_rim"]
    pt["ft_trips"] = p["ft_trips"]
    pt["transition"] = p["transition_fga"]
    pt["own_threes"] = p["fga_three"] * (1 - a_three)
    pt["cs_threes"] = p["fga_three"] * a_three
    pt["cs_mid"] = p["fga_mid"] * a_mid
    pt["steals"] = p["steals"]
    pt["blocks"] = p["blocks"]
    pt["drb"] = p["drb"]
    pt["orb"] = p["orb"]
    pt["putbacks"] = p["putbacks"]

    if mode == "coarse":
        # --- 3 coarse proxies (2015-2025) ---
        rim_not_putback = (p["fga_rim"] - p["putbacks"]).clip(lower=0)
        pt["unassisted_rim"] = rim_not_putback * (1 - a_rim)
        pt["unassisted_mid"] = p["fga_mid"] * (1 - a_mid)
        pt["assisted_rim"] = rim_not_putback * a_rim
    else:
        # --- 8 tagged play types (2026) ---
        # cut & roll: plain rim attempts x his assisted share of plain rim makes.
        # Shrunk toward the national RIM share (the spec does not name a separate target).
        a_plain = shrunk_assisted_share(p["plain_rim_fgm_ast"], p["plain_rim_fgm"],
                                        national["rim"], k)
        pt["driving_layups"] = p["driving_layups"]
        pt["pullups_2"] = p["pullups_2"]
        pt["pullup_range_2s"] = p["pullup_range_2s"]
        pt["floaters"] = p["floaters"]
        pt["pullups_3"] = p["pullups_3"]
        pt["cut_roll"] = p["plain_rim_fga"] * a_plain
        pt["tip_ins"] = p["tip_ins"]
        pt["hooks_turnarounds"] = p["hooks_turnarounds"]
    return pt


# ---------------------------------------------------------------------------
# 2. play types -> rates per 100
# ---------------------------------------------------------------------------

def _per_100(count, poss):
    """count / poss x 100, blank where there are no possessions to divide by."""
    poss = poss.astype(float).where(poss > 0)          # 0 or missing -> NaN
    return count.astype(float) / poss * 100


def build_rates(play_types, pooled, mode):
    """Rate per 100 for every play type, using the right denominator for each."""
    rates = pd.DataFrame(index=play_types.index)
    for col in play_types_for(mode):
        if col in DEFENSIVE:
            denom = pooled["def_poss"]
        elif col in FULL_SEASON_TAGGED:
            denom = pooled["off_poss_this"]
        elif col in TAGGED:
            denom = pooled["tagged_off_poss"]          # NaN / 0 -> blank rate
        else:
            denom = pooled["off_poss"]
        rates[col] = _per_100(play_types[col], denom)
    return rates


# ---------------------------------------------------------------------------
# 3. rates -> percentiles
# ---------------------------------------------------------------------------

def percentile_vs(values, reference):
    """Share of `reference` values strictly LOWER than each value (0 to 1).

    values     the numbers to place (a pandas Series; NaN stays NaN)
    reference  the population to compare against (NaNs are ignored)

    Example: reference [1, 2, 3, 4], value 3 -> 2 of 4 are lower -> 0.50
    """
    ref = np.sort(reference.dropna().to_numpy(dtype=float))
    if len(ref) == 0:
        return pd.Series(np.nan, index=values.index)
    v = values.to_numpy(dtype=float)
    lower = np.searchsorted(ref, v, side="left")       # how many ref values are < v
    out = lower / len(ref)
    out[np.isnan(v)] = np.nan
    return pd.Series(out, index=values.index)


def build_percentiles(rates, qualified):
    """Percentile of every rate column against the qualified players' rates."""
    return pd.DataFrame({col: percentile_vs(rates[col], rates.loc[qualified, col])
                         for col in rates.columns}, index=rates.index)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def compute_play_types(pooled, national, mode, k=5):
    """Run all three conversions. Returns one wide DataFrame, one row per player:

        player_id, season, mode, qualified, read,
        n_<play type>     the play-type count
        rate_<play type>  per 100
        pctl_<play type>  0-1 against qualified players
    """
    pooled = pooled.reset_index(drop=True)
    pt = build_play_types(pooled, national, mode, k)
    rates = build_rates(pt, pooled, mode)
    pctls = build_percentiles(rates, pooled["qualified"].astype(bool))

    out = pooled[["player_id", "season", "qualified", "read"]].copy()
    out["mode"] = mode
    out = pd.concat([out, pt.add_prefix("n_"), rates.add_prefix("rate_"),
                     pctls.add_prefix("pctl_")], axis=1)
    return out
