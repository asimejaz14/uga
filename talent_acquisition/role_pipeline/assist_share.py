"""
Step 2 — national assisted share, per season and shot zone.

Why it exists:
    A player's assisted share is shrunk toward the national share over 5 makes
    (spec 2.4):
        a = (his assisted makes + 5 x national share) / (his makes + 5)
    A player with 2 makes can't tell us much on his own, so the "+5" pulls him
    toward the league; a player with 200 makes barely moves.
    This step produces the "national share" in that formula.

Formula, for each season and zone (rim, mid, three):
    ast_share = sum of assisted makes in that zone / sum of all makes in that zone
                (summed over every player in player_season_counts)

Output columns: season, zone, ast_share
"""
import pandas as pd

# zone -> (assisted makes column, all makes column) in player_season_counts
ZONES = {
    "rim":   ("fgm_rim_ast",   "fgm_rim"),
    "mid":   ("fgm_mid_ast",   "fgm_mid"),
    "three": ("fgm_three_ast", "fgm_three"),
}


def national_assist_share(counts):
    """Main entry point for Step 2. Returns the NationalAssistShare rows."""
    rows = []
    for season, g in counts.groupby("season"):
        for zone, (ast_col, make_col) in ZONES.items():
            makes = g[make_col].sum()
            if makes == 0:
                # No makes in a whole season and zone means the data is broken, not zero:
                # stop loudly instead of writing a share that would silently mislead.
                raise ValueError(f"season {season}: no {zone} makes, cannot compute share")
            rows.append({"season": int(season), "zone": zone,
                         "ast_share": g[ast_col].sum() / makes})
    return pd.DataFrame(rows, columns=["season", "zone", "ast_share"])


def shrunk_assisted_share(assisted_makes, makes, national_share, k=5):
    """The per-player formula this table feeds (used from Step 4 on; here for reference).

        a = (assisted_makes + k x national_share) / (makes + k)

    Works on numbers or on whole pandas columns.
    Example: 3 assisted of 4 makes, national 0.60 ->  (3 + 3.0) / (4 + 5) = 0.667
    """
    return (assisted_makes + k * national_share) / (makes + k)
