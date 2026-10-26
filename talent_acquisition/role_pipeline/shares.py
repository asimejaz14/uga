"""
Step 5 — teammate shares: lead, lead2, inside, inside2, front.

The question (spec 2.6): "who does he do it beside?"
Two players can pass the same amount and still not be the same player: if one always
has a better passer next to him, he is not the one running the offence. We find that
out by comparing him with the other four players on the floor, possession by possession.

For every possession we look at the five players of one team and ask each player:

    lead     were you the #1 passer of the five?          (assists per 100)
    lead2    were you #1 or #2?
    inside   were you the #1 interior player of the five?  (ORB + blocks + putbacks per 100)
    inside2  were you #1 or #2?
    front    were you one of the two TALLEST of the five?  (height, "plays the 4-5")

A share = (possessions where the answer was yes) / (possessions counted).

Important details from the spec
-------------------------------
* The ranking uses each player's SEASON rate (from Step 4), not what happened in
  that possession. The possession only tells us who was on the floor together.
* A possession is counted only when 4 or more of the five have a "read"
  (300+ pooled possessions). Fewer than that, and the comparison isn't trustworthy.
* A share needs 200+ counted possessions. Below that it is left blank (missing),
  and every rule that uses it is skipped later.

Choices the spec does not spell out (each one is a single constant below):
* SIDE = offensive possessions only. Role is about how he plays offence, and the
  lineup is the same five on both ends anyway.
* A player WITHOUT a read is ranked last on that possession (he can't be #1).
* Ties: "rank = 1 + how many of the other four are strictly higher". Two players with
  exactly the same rate are both #1.
* inside rate = rate_orb + rate_blocks + rate_putbacks (each per 100, from Step 4).
* front needs all five heights known; possessions with a missing height are not
  counted for front (they still count for lead / inside).
"""
import numpy as np
import pandas as pd

from .possessions import valid_possessions

SIDE = "off"                 # which five to look at: "off" = the team with the ball
MIN_READS = 4                # SHARE_MIN_READS: 4 of the 5 need a read
MIN_POSS = 200               # SHARE_MIN_POSS: share needs 200+ counted possessions


# ---------------------------------------------------------------------------
# Small building blocks
# ---------------------------------------------------------------------------

def lineup_matrix(possessions, games, side=SIDE):
    """The five player IDs of every valid possession, as a numpy array (n x 5).

    Uses the same filters as Step 1: regular season, no tournament, no garbage time,
    and the side must resolve to five distinct players.
    """
    df = valid_possessions(possessions, games)
    df = df[df[f"{side}_ok"]]
    cols = [f"{side}_p{i}" for i in range(1, 6)]
    return df[cols].to_numpy(dtype="int64")


def look_up(lineups, values_by_player):
    """Replace every player ID in the n x 5 lineup array with a value about that player.

    Example: lineups [[1, 2, 3, 4, 5]] and values {1: 9.0, 2: 3.0, ...}
             -> [[9.0, 3.0, ...]]
    A player not in the dictionary gets NaN.
    """
    flat = pd.Series(lineups.ravel()).map(values_by_player)
    return flat.to_numpy(dtype="float64").reshape(lineups.shape)


def rank_in_five(values):
    """Rank of each player inside his five: 1 = highest value.

    rank = 1 + how many of the OTHER four have a strictly higher value.

        values [10, 4, 7, 4, 2]  ->  ranks [1, 3, 2, 3, 5]

    How it works: for each pair (me, other) we ask "is other > me?" and add up the
    yeses. values[:, None, :] > values[:, :, None] builds that 5 x 5 yes/no table for
    every possession at once. NaN is never "higher", so put NaN in as -inf first if
    you want it ranked last.
    """
    higher = values[:, None, :] > values[:, :, None]     # [possession, me, other]
    return 1 + higher.sum(axis=2)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def compute_shares(possessions, games, play_types, pooled, season,
                   min_reads=MIN_READS, min_poss=MIN_POSS):
    """Main entry point for Step 5.

    possessions  Possession rows for this season
    games        Game rows for this season
    play_types   Step 4 output for this season (rate_assists, rate_orb, ...)
    pooled       Step 3 output for this season (read, height_in)

    Returns one row per player who appears in a counted possession:
        player_id, season, valid_poss, lead, lead2, inside, inside2, front, front_poss
    """
    lineups = lineup_matrix(possessions[possessions["season"] == season],
                            games[games["season"] == season])

    # --- 1. the numbers we rank on, per player ---------------------------------
    pt = play_types.set_index("player_id")
    has_read = pooled.set_index("player_id")["read"].astype(bool)
    height = pooled.set_index("player_id")["height_in"]

    passing = pt["rate_assists"]
    interior = pt["rate_orb"] + pt["rate_blocks"] + pt["rate_putbacks"]

    # A player without a read is ranked last: give him -infinity.
    passing = passing.where(has_read, -np.inf)
    interior = interior.where(has_read, -np.inf)

    # --- 2. swap IDs for numbers, possession by possession ---------------------
    read_5 = look_up(lineups, has_read.astype(float).to_dict()) == 1
    pass_5 = look_up(lineups, passing.to_dict())
    inside_5 = look_up(lineups, interior.to_dict())
    height_5 = look_up(lineups, height.to_dict())

    # Players we know nothing about (no Step 4 row) are also ranked last.
    pass_5 = np.nan_to_num(pass_5, nan=-np.inf)
    inside_5 = np.nan_to_num(inside_5, nan=-np.inf)

    # --- 3. which possessions count ---------------------------------------------
    counted = read_5.sum(axis=1) >= min_reads          # 4+ of the five have a read
    heights_known = ~np.isnan(height_5).any(axis=1)    # all five heights known

    # --- 4. rank every player inside his five -----------------------------------
    pass_rank = rank_in_five(pass_5)
    inside_rank = rank_in_five(inside_5)
    tall_rank = rank_in_five(np.nan_to_num(height_5, nan=-np.inf))

    # --- 5. one row per (possession, player) -----------------------------------
    # Each array below is n x 5; ravel() flattens them in the same order, so row i
    # of every column belongs to the same player in the same possession.
    long = pd.DataFrame({
        "player_id": lineups.ravel(),
        "counted": np.repeat(counted, 5),
        "front_counted": np.repeat(counted & heights_known, 5),
        "lead": (pass_rank == 1).ravel(),
        "lead2": (pass_rank <= 2).ravel(),
        "inside": (inside_rank == 1).ravel(),
        "inside2": (inside_rank <= 2).ravel(),
        "front": (tall_rank <= 2).ravel(),             # slots 4-5 = two tallest
    })

    # --- 6. add up per player ---------------------------------------------------
    c = long[long["counted"]]
    out = c.groupby("player_id").agg(
        valid_poss=("counted", "size"),
        lead=("lead", "mean"),         # mean of True/False = share of True
        lead2=("lead2", "mean"),
        inside=("inside", "mean"),
        inside2=("inside2", "mean"),
    )
    f = long[long["front_counted"]]
    front = f.groupby("player_id").agg(front_poss=("front", "size"), front=("front", "mean"))
    out = out.join(front, how="left")
    out["front_poss"] = out["front_poss"].fillna(0).astype(int)

    # --- 7. under 200 counted possessions -> missing ---------------------------
    too_few = out["valid_poss"] < min_poss
    out.loc[too_few, ["lead", "lead2", "inside", "inside2"]] = np.nan
    out.loc[out["front_poss"] < min_poss, "front"] = np.nan

    out["season"] = season
    return out.reset_index()[["player_id", "season", "valid_poss", "lead", "lead2",
                              "inside", "inside2", "front", "front_poss"]]
