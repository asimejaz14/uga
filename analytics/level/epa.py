"""
Level stage 1-2: har player ke season counts ko 11 EPA PIECES mein badalna
(spec 3.3, 3.4).

EPA = Expected Points Added: average possession (1.075 points) ke muqable
player ne kitne extra points banaye ya ganwaye.

Hamare paas event-level data nahi, sirf season counts hain (L-01). Ye kaafi
hai, kyunke har event ki qeemat season ke andar fixed hai: "har event ki
qeemat ka jama" = "count x qeemat".

Ye file PURE PYTHON hai (D-13).

Qeematein (constants.py):
    unassisted make      points - 1.075           (shooter)
    assisted make        points - xPTS(zone)      (shooter)
                         xPTS(zone) - 1.075       (passer -> Creation)
    miss                 -0.774
    FT made / missed     +0.530 / -0.470
    off rebound          +0.785   (A-04)
    steal / turnover     +1.075 / -1.075
    block                +0.750
    foul to the line     -(FTs awarded) x league FT%
    technical            -2 x league FT%

Misses ka bantwara (Self-creation / Shooting / Finishing) assisted share se
ek ESTIMATE hai (L-07), kyunke ESPN miss par pass record nahi karta.
"""
from analytics.constants import (
    BLOCK_VALUE, FT_BASELINE, FT_MADE_VALUE, FT_MISSED_VALUE, MISS_VALUE,
    OFF_REBOUND_VALUE, PPP, SHOT_POINTS, STEAL_VALUE, TECHNICAL_FREE_THROWS,
    TURNOVER_VALUE,
)
from analytics.role.play_types import shrunk_share

# PlayerSeasonLevel ke field names, isi order mein
PIECES = (
    "epa_self_creation", "epa_shooting", "epa_finishing", "epa_ft_drawing",
    "epa_ft_making", "epa_creation", "epa_ball_security", "epa_off_rebounds",
    "epa_steals", "epa_blocks", "epa_discipline",
)


def epa_pieces(c, league):
    """
    c:      ek player-season ke counts (dict; PlayerSeasonCounts ke field names)
    league: level.league.LeagueValues (is season ki)

    Wapas: {piece field name: points}  (11 pieces; jama = EPA total)
    """
    xpts = league.xpts
    ft_pct = league.league_ft_pct

    # --- Assisted shares (shrunk), spec 3.4: rim aur jumper (mid + three) ---
    a_rim = shrunk_share(c["fgm_rim_ast"], c["fgm_rim"], league.national_share["rim"])
    a_jumper = shrunk_share(
        c["fgm_mid_ast"] + c["fgm_three_ast"],
        c["fgm_mid"] + c["fgm_three"],
        league.ast_share_jumper,
    )

    rim_misses = c["fga_rim"] - c["fgm_rim"]
    jumper_misses = (c["fga_mid"] - c["fgm_mid"]) + (c["fga_three"] - c["fgm_three"])

    # --- Makes: unassisted vs assisted ---
    unassisted = {
        "rim": c["fgm_rim"] - c["fgm_rim_ast"],
        "mid": c["fgm_mid"] - c["fgm_mid_ast"],
        "three": c["fgm_three"] - c["fgm_three_ast"],
    }

    self_creation = (
        sum(unassisted[z] * (SHOT_POINTS[z] - PPP) for z in SHOT_POINTS)
        + rim_misses * (1 - a_rim) * MISS_VALUE
        + jumper_misses * (1 - a_jumper) * MISS_VALUE
    )
    shooting = (
        c["fgm_mid_ast"] * (SHOT_POINTS["mid"] - xpts["mid"])
        + c["fgm_three_ast"] * (SHOT_POINTS["three"] - xpts["three"])
        + jumper_misses * a_jumper * MISS_VALUE
    )
    finishing = (
        c["fgm_rim_ast"] * (SHOT_POINTS["rim"] - xpts["rim"])
        + rim_misses * a_rim * MISS_VALUE
    )

    # --- Free throws: drawing + making = FT EPA ---
    ft_misses = c["fta"] - c["ftm"]
    ft_epa = c["ftm"] * FT_MADE_VALUE + ft_misses * FT_MISSED_VALUE
    ft_drawing = c["fta"] * (ft_pct - FT_BASELINE)
    ft_making = ft_epa - ft_drawing

    # --- Creation: har assist ka passer wala hissa (A-05: mid = baaqi) ---
    ast_mid = c["assists"] - c["ast_to_rim"] - c["ast_to_three"]
    creation = (
        c["ast_to_rim"] * (xpts["rim"] - PPP)
        + c["ast_to_three"] * (xpts["three"] - PPP)
        + ast_mid * (xpts["mid"] - PPP)
    )

    discipline = (
        -c["fts_conceded"] * ft_pct
        - c["technicals"] * TECHNICAL_FREE_THROWS * ft_pct
    )

    return {
        "epa_self_creation": self_creation,
        "epa_shooting": shooting,
        "epa_finishing": finishing,
        "epa_ft_drawing": ft_drawing,
        "epa_ft_making": ft_making,
        "epa_creation": creation,
        "epa_ball_security": c["turnovers"] * TURNOVER_VALUE,
        "epa_off_rebounds": c["orb"] * OFF_REBOUND_VALUE,
        "epa_steals": c["steals"] * STEAL_VALUE,
        "epa_blocks": c["blocks"] * BLOCK_VALUE,
        "epa_discipline": discipline,
    }


def pbp_points(c):
    """Play-by-play ke mutabiq player ke points (coverage ka numerator)."""
    return 2 * c["fgm_rim"] + 2 * c["fgm_mid"] + 3 * c["fgm_three"] + c["ftm"]


def coverage(c, box_points):
    """pbp points / box points. Box points 0 ho to None (rate nahi ban sakta)."""
    if not box_points:
        return None
    return pbp_points(c) / box_points


def per_40(value, minutes):
    """value / minutes * 40. Minutes 0 ho to None."""
    if not minutes:
        return None
    return value / minutes * 40
