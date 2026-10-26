"""
Level ke steps ko JORNE wala module (Step 2).

    league values (4a)  ->  har player ke 11 pieces + EPA/40
    Role families       ->  bench band -> replacement (season +-1 pooled)
    points per win      ->  surplus -> WAR -> tier

Replacement ko pas-pados ke seasons chahiyein (family gap s-1, s, s+1), is
liye un seasons ka EPA bhi nikalna parta hai. build_level() ye khud karta hai.

Ye file database PARHTI hai (loaders), likhti nahi.
"""
from dataclasses import dataclass, field

from analytics import loaders
from analytics.constants import (
    COVERAGE_MIN, LEVEL_FIRST_SEASON, LEVEL_QUALIFIED_MINUTES,
)
from analytics.level.epa import coverage, epa_pieces, per_40
from analytics.level.league import fit_points_per_win, league_values
from analytics.level.replacement import BenchPlayer, in_bench_band, replacement_levels
from analytics.level.war import tier_for, war, war_per_40


@dataclass
class LevelPlayer:
    player_id: int
    team_id: int
    minutes: int
    is_d1: bool
    pieces: dict
    epa_total: float
    coverage: float
    epa_per40: float
    family: str = None
    placement_id: int = None
    # Target season ke liye neeche bharte hain:
    is_rated: bool = False
    is_qualified: bool = False
    surplus_per40: float = None
    war_per40: float = None
    war: float = None
    tier: str = None


@dataclass
class LevelSeason:
    season: int
    league: object                 # LeagueValues
    players: dict                  # {player_id: LevelPlayer}
    role_run: object = None        # CalculationRun (Role) ya None
    ppw: object = None             # PointsPerWinFit
    replacement: object = None     # Replacement
    history_complete: bool = True
    d1_teams: int = 0
    extra: dict = field(default_factory=dict)


def season_players(season):
    """Ek season: league values + har player ke pieces aur EPA/40 (family ke saath)."""
    league = league_values(loaders.league_shot_totals(season), loaders.national_assist_shares(season))
    role_run, families = loaders.role_families(season)

    players = {}
    for row in loaders.level_rows(season):
        pieces = epa_pieces(row["counts"], league)
        total = sum(pieces.values())
        placement_id, family = families.get(row["player_id"], (None, None))
        players[row["player_id"]] = LevelPlayer(
            player_id=row["player_id"],
            team_id=row["team_id"],
            minutes=row["minutes"],
            is_d1=row["is_d1"],
            pieces=pieces,
            epa_total=total,
            coverage=coverage(row["counts"], row["points"]),
            epa_per40=per_40(total, row["minutes"]),
            family=family,
            placement_id=placement_id,
        )
    return LevelSeason(season=season, league=league, players=players, role_run=role_run)


def bench_of(level_season):
    """Is season ke bench band ke players (BenchPlayer list)."""
    return [
        BenchPlayer(season=level_season.season, epa_per40=p.epa_per40, family=p.family)
        for p in level_season.players.values()
        if in_bench_band(p.minutes, p.is_d1) and p.epa_per40 is not None
    ]


def build_level(target_seasons):
    """
    Target seasons ka poora Level. Wapas: {season: LevelSeason}.
    Target season ki Role run zaroori hai (family); pas-pados ki Role run na ho
    to un ke bench players family gap mein nahi ginte.
    """
    available = loaders.seasons_with_counts()
    needed = sorted({s for t in target_seasons for s in (t - 1, t, t + 1) if s in available})
    by_season = {s: season_players(s) for s in needed}
    bench_by_season = {s: bench_of(by_season[s]) for s in needed}

    results = {}
    for season in target_seasons:
        data = by_season[season]
        if data.role_run is None:
            raise ValueError(f"Season {season} ki kamyab Role run nahi. Pehle compute_role chalayein.")

        window = {s: bench_by_season[s] for s in (season - 1, season, season + 1) if s in bench_by_season}
        data.replacement = replacement_levels(season, window)
        data.ppw = fit_points_per_win(loaders.d1_team_records(season))
        data.d1_teams = len(loaders.d1_team_ids(season))
        # Family gap ko s-1 chahiye; spec ka pehla season (2015) clip hota hai
        data.history_complete = (season - 1 in available) or season == LEVEL_FIRST_SEASON

        for p in data.players.values():
            p.is_rated = p.coverage is not None and p.coverage >= COVERAGE_MIN
            p.is_qualified = p.is_rated and p.is_d1 and p.minutes >= LEVEL_QUALIFIED_MINUTES
            if not p.is_rated or p.epa_per40 is None:
                continue  # not rated: surplus / WAR / tier nahi
            p.surplus_per40 = p.epa_per40 - data.replacement.for_family(p.family)
            p.war_per40 = war_per_40(p.surplus_per40, data.ppw.points_per_win)
            p.war = war(p.war_per40, p.minutes)
            p.tier = tier_for(p.war_per40)
        results[season] = data
    return results
