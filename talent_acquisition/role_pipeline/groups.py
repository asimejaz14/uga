"""
Step 6a — the seven groups and their scores.

21 play types are too many to map onto nine roles directly, so they are bundled into
seven kinds of basketball work (spec 2.7, Stage A). Then each player gets one score
per group (Stage B):

    raw score   = mean of his TWO HIGHEST play-type percentiles in the group
                  (only one present -> that one; none -> blank)

    group score = share of qualified players with a lower raw score IN THAT GROUP
                  (the same "percentile" idea as Step 4, done again)

Why the top two?
    Self-creation has 8 play types; nobody does all eight. A plain mean would punish
    big groups. The top two reward what he does without charging him for what he doesn't.

Why re-percentile?
    Steals has ONE play type, Self-creation EIGHT. Their raw scores are not on the same
    scale. Turning each into a percentile *within its own group* fixes that, so a short
    group can't win on variance alone.

Worked example (spec 2.9), Creation group:
    percentiles 0.85, 0.78, 0.60 -> top two 0.85, 0.78 -> raw 0.815 -> group score 0.88
"""
import warnings

import numpy as np
import pandas as pd

from .play_types import percentile_vs

GROUP_NAMES = ["creation", "self_creation", "shooting", "steals",
               "def_glass", "blocks", "inside"]

# 2026 — full rules (tagged play types)
GROUPS_FULL = {
    "creation":      ["assists", "ast_to_three", "ast_to_rim"],
    "self_creation": ["driving_layups", "pullups_2", "pullup_range_2s", "floaters",
                      "ft_trips", "transition", "own_threes", "pullups_3"],
    "shooting":      ["cs_threes", "cs_mid"],
    "steals":        ["steals"],
    "def_glass":     ["drb"],
    "blocks":        ["blocks"],
    "inside":        ["orb", "putbacks", "tip_ins", "cut_roll", "hooks_turnarounds"],
}

# 2015-2025 — coarse rules (proxies instead of tags)
GROUPS_COARSE = {
    "creation":      ["assists", "ast_to_three", "ast_to_rim"],
    "self_creation": ["unassisted_rim", "unassisted_mid", "ft_trips", "transition", "own_threes"],
    "shooting":      ["cs_threes", "cs_mid"],
    "steals":        ["steals"],
    "def_glass":     ["drb"],
    "blocks":        ["blocks"],
    "inside":        ["orb", "putbacks", "assisted_rim"],
}


def groups_for(mode):
    return GROUPS_FULL if mode == "full" else GROUPS_COARSE


def mean_of_top_two(pctls):
    """Row by row: the mean of the two highest values, ignoring blanks.

        [0.85, 0.78, 0.60]  -> (0.85 + 0.78) / 2 = 0.815
        [0.40, NaN,  NaN ]  -> 0.40       (only one present)
        [NaN,  NaN,  NaN ]  -> NaN

    How: sort each row from high to low (blanks pushed to the end), keep the first
    two columns, and average them while skipping blanks.
    """
    arr = pctls.to_numpy(dtype=float)
    arr = -np.sort(-np.nan_to_num(arr, nan=-np.inf), axis=1)   # high -> low, blanks last
    top2 = arr[:, :2]
    top2[np.isinf(top2)] = np.nan
    with warnings.catch_warnings():                    # an all-blank row is fine: -> NaN
        warnings.simplefilter("ignore", RuntimeWarning)
        return pd.Series(np.nanmean(top2, axis=1), index=pctls.index)


def compute_group_scores(play_types, mode):
    """Main entry point for Step 6a.

    play_types  Step 4 output (needs pctl_<play type> and qualified)
    Returns the same rows with raw_<group> and score_<group> for the seven groups.
    """
    out = play_types[["player_id", "season", "qualified"]].copy()
    qualified = play_types["qualified"].astype(bool)

    for group, members in groups_for(mode).items():
        cols = [f"pctl_{m}" for m in members]
        raw = mean_of_top_two(play_types[cols])
        out[f"raw_{group}"] = raw
        out[f"score_{group}"] = percentile_vs(raw, raw[qualified])   # within this group only
    return out
