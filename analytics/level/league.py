"""
Level ke SEASON-WIDE numbers: league FT%, har zone ka xPTS, national jumper
share, aur points per win.

Ye file PURE PYTHON hai (D-13): na database, na Django models. Data
analytics/loaders.py se aata hai. Is liye in functions ko bina database
ke test kiya ja sakta hai (analytics/tests/test_league.py).

Validation (2026, spec):
    xPTS rim 1.3100 · mid 0.9548 · three 1.2139 · league FT% .7223   (V-10..V-13)
    points per win: 365 teams, y = 14.75 + 0.02399x, r .933, 41.69   (V-16, V-17)
"""
import statistics
from dataclasses import dataclass

from analytics.constants import (
    OREB_RECOVERY_RATE, PPP, PPW_GAMES_SCALE, PPW_MIN_GAMES, SHOT_POINTS,
)


# ---------------------------------------------------------------------------
# Shot values
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LeagueShotTotals:
    """Ek season ke SAB players ke counts ka jama (Q-06: population = all)."""
    fga_rim: int
    fgm_rim: int
    fga_mid: int
    fgm_mid: int
    fga_three: int
    fgm_three: int
    fta: int
    ftm: int


@dataclass(frozen=True)
class LeagueValues:
    """Season ke shot prices aur shares. Level ke har player par yahi lagte hain."""
    league_ft_pct: float
    fg_pct: dict           # {"rim": 0.594, "mid": ..., "three": ...}
    xpts: dict             # {"rim": 1.3103, "mid": ..., "three": ...}
    national_share: dict   # {"rim": 0.4262, "mid": ..., "three": ...}
    ast_share_jumper: float


def expected_points(points, fg_pct):
    """
    Ek shot ki expected value (spec 3.4):

        xPTS = points * FG%  +  (1 - FG%) * 0.28 * 1.075
               └ make se ┘     └ miss ke baad 28% ball wapas ┘

    Misaal: rim, FG% 0.60 -> 2*0.60 + 0.40*0.301 = 1.3204
    """
    return points * fg_pct + (1 - fg_pct) * OREB_RECOVERY_RATE * PPP


def jumper_share(national_share, fgm_mid, fgm_three):
    """
    National jumper (mid + three) assisted share, zone shares ko league makes
    se weight kar ke. Is tarah ye data engineer ki NationalAssistShare table
    se consistent rehta hai (hum zone shares ussi table se lete hain).

        jumper = (share_mid * fgm_mid + share_three * fgm_three) / (fgm_mid + fgm_three)
    """
    makes = fgm_mid + fgm_three
    if makes == 0:
        raise ValueError("Jumper makes 0 hain; jumper share nahi ban sakta.")
    return (national_share["mid"] * fgm_mid + national_share["three"] * fgm_three) / makes


def league_values(totals, national_share):
    """
    Season ke league values.

    totals:         LeagueShotTotals (sab players ka jama)
    national_share: {"rim": float, "mid": float, "three": float}
                    data engineer ki NationalAssistShare table se (as-is).
    """
    attempts = {"rim": totals.fga_rim, "mid": totals.fga_mid, "three": totals.fga_three}
    makes = {"rim": totals.fgm_rim, "mid": totals.fgm_mid, "three": totals.fgm_three}

    fg_pct = {}
    for zone in SHOT_POINTS:
        if attempts[zone] == 0:
            raise ValueError(f"{zone} attempts 0 hain; FG% nahi ban sakta.")
        fg_pct[zone] = makes[zone] / attempts[zone]

    if totals.fta == 0:
        raise ValueError("FTA 0 hain; league FT% nahi ban sakta.")

    missing = set(SHOT_POINTS) - set(national_share)
    if missing:
        raise ValueError(f"National share missing zones: {sorted(missing)}")

    return LeagueValues(
        league_ft_pct=totals.ftm / totals.fta,
        fg_pct=fg_pct,
        xpts={zone: expected_points(SHOT_POINTS[zone], fg_pct[zone]) for zone in SHOT_POINTS},
        national_share=dict(national_share),
        ast_share_jumper=jumper_share(national_share, totals.fgm_mid, totals.fgm_three),
    )


# ---------------------------------------------------------------------------
# Points per win
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TeamRecord:
    """Ek team ka regular-season record (sirf D1 teams loader se aati hain)."""
    team_id: int
    games: int
    wins: int
    point_margin: int    # season ka kul margin (scored - allowed)


@dataclass(frozen=True)
class PointsPerWinFit:
    teams: int
    intercept: float     # a
    slope: float         # b
    r: float
    points_per_win: float


def fit_points_per_win(records):
    """
    Scoreboard se points per win (spec 3.8):

        har team (10+ games):  x = margin per game * 31,  y = wins per game * 31
        least squares:         y = a + b*x
        points per win       = 1 / b

    b batata hai ek point margin se kitni jeet barhti hai; 1/b batata hai
    ek jeet kitne points ki hai.
    """
    eligible = [r for r in records if r.games >= PPW_MIN_GAMES]
    if len(eligible) < 2:
        raise ValueError(f"Regression ke liye kam az kam 2 teams chahiyein, mili {len(eligible)}.")

    xs = [r.point_margin / r.games * PPW_GAMES_SCALE for r in eligible]
    ys = [r.wins / r.games * PPW_GAMES_SCALE for r in eligible]

    slope, intercept = statistics.linear_regression(xs, ys)
    if slope <= 0:
        raise ValueError(f"Slope {slope} positive nahi; data mein kuch ghalat hai.")

    return PointsPerWinFit(
        teams=len(eligible),
        intercept=intercept,
        slope=slope,
        r=statistics.correlation(xs, ys),
        points_per_win=1 / slope,
    )