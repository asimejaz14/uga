"""
Step 1 — possessions on the floor per player-season.

Spec (v9.1, section 2.3):
  * Regular season only: season_type = 2 and no tournament id.
  * A possession counts for a player only when HIS SIDE resolves to five distinct
    players and it is not garbage time.
  * Offence is counted per 100 offensive possessions, defence per 100 defensive
    possessions, so we need both totals.
  * 2026 tagged play types are rated per 100 possessions IN TAGGED GAMES, so we also
    count offensive possessions in games that carry shot tags (tagged_off_poss).

Output (one row per player-season):
    player_id, season, team_id, off_poss, def_poss, tagged_off_poss
tagged_off_poss is NULL for seasons with no tagged games at all (everything before 2026).
"""
import numpy as np
import pandas as pd

OFF_COLS = [f"off_p{i}" for i in range(1, 6)]
DEF_COLS = [f"def_p{i}" for i in range(1, 6)]


def five_distinct(possessions, cols):
    """True for each row whose 5 player columns are all present and all different.

    Example:  [11, 12, 13, 14, 15] -> True
              [11, 12, 13, 14, NA] -> False  (only four known)
              [11, 12, 13, 14, 14] -> False  (same player twice: bad lineup data)
    """
    block = possessions[cols]
    all_present = block.notna().all(axis=1)
    # Sort each row; if any two neighbours are equal, the row has a duplicate.
    arr = np.sort(block.astype("float64").to_numpy(), axis=1)
    no_duplicates = (np.diff(arr, axis=1) != 0).all(axis=1)
    return all_present & no_duplicates


def valid_possessions(possessions, games):
    """Keep regular-season, non-tournament, non-garbage possessions.

    Adds three columns used later:
        has_shot_tags  - copied from the game
        off_ok         - offence side resolves to five distinct players
        def_ok         - defence side resolves to five distinct players
    The two sides are checked separately: a broken defence row must not cost the
    offence players their possession, and vice versa.
    """
    regular = games[(games["season_type"] == 2) & games["tournament_id"].isna()]
    df = possessions.merge(regular[["game_id", "has_shot_tags"]], on="game_id", how="inner")
    df = df[~df["garbage_time"]].copy()
    df["off_ok"] = five_distinct(df, OFF_COLS)
    df["def_ok"] = five_distinct(df, DEF_COLS)
    return df


def _long(df, side):
    """Turn the 5 player columns of one side into one row per (possession, player).

    Input  (one possession):  season | off_team_id | off_p1 .. off_p5 | has_shot_tags
    Output (five rows):       season | team_id | player_id | has_shot_tags
    """
    cols = OFF_COLS if side == "off" else DEF_COLS
    ok = df[df[f"{side}_ok"]]
    long = ok.melt(id_vars=["season", f"{side}_team_id", "has_shot_tags"],
                   value_vars=cols, value_name="player_id")
    long = long.rename(columns={f"{side}_team_id": "team_id"})
    long["player_id"] = long["player_id"].astype("int64")
    return long[["season", "team_id", "player_id", "has_shot_tags"]]


def count_player_possessions(possessions, games):
    """Main entry point for Step 1. Returns the PlayerSeasonPossessions rows."""
    df = valid_possessions(possessions, games)
    off = _long(df, "off")
    de = _long(df, "def")

    keys = ["player_id", "season"]
    off_poss = off.groupby(keys).size().rename("off_poss")
    def_poss = de.groupby(keys).size().rename("def_poss")
    tagged = off[off["has_shot_tags"]].groupby(keys).size().rename("tagged_off_poss")

    # Outer join: a player can (rarely) appear only on one side; the other count is 0.
    out = pd.concat([off_poss, def_poss], axis=1).fillna(0).astype("int64")

    # tagged_off_poss: 0 if the season HAS tagged games but he played none of them,
    # NULL if the season has no tagged games at all (pre-2026).
    out = out.join(tagged)
    tagged_seasons = set(games.loc[games["has_shot_tags"], "season"])
    in_tagged_season = out.index.get_level_values("season").isin(tagged_seasons)
    out["tagged_off_poss"] = out["tagged_off_poss"].astype("Int64")
    out.loc[in_tagged_season, "tagged_off_poss"] = out.loc[in_tagged_season, "tagged_off_poss"].fillna(0)

    out["team_id"] = main_team(pd.concat([off, de]))
    return out.reset_index()[["player_id", "season", "team_id",
                              "off_poss", "def_poss", "tagged_off_poss"]]


def main_team(long):
    """The team a player spent most possessions with that season.

    The table holds one row per player-season, so a mid-season move needs one team.
    Ties go to the lower team_id, just so the result is repeatable.
    """
    n = long.groupby(["player_id", "season", "team_id"]).size().rename("n").reset_index()
    n = n.sort_values(["player_id", "season", "n", "team_id"], ascending=[True, True, False, True])
    return n.drop_duplicates(["player_id", "season"]).set_index(["player_id", "season"])["team_id"]
