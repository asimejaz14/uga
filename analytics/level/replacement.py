"""
Level stage 4: replacement level (spec 3.6).

Replacement = woh player jo team ko "muft" milta hai: D1 team ka bench
player (is season 50-149 minutes). Us ka average EPA/40 replacement level hai.

    overall(s)  = season s ke bench players ke EPA/40 ka simple mean
    gap(f)      = family f ke bench players ka (EPA/40 - apne season ka overall),
                  seasons s-1, s, s+1 par pool, bench players se weighted
    replacement(s, f) = overall(s) + gap(f)            (A-16)
    family nahi        -> overall(s)

"Weighted by bench players" ka matlab: har bench player ka ek vote. Teen
seasons ke saare family-f bench players ke farq ka seedha mean.

2026 spec: overall -1.75 · guards -2.16 · wings -1.63 · bigs -1.31 · 556 bench (V-14, V-15)

Ye file PURE PYTHON hai (D-13).
"""
import statistics
from dataclasses import dataclass

from analytics.choices import Family
from analytics.constants import BENCH_MAX_MINUTES, BENCH_MIN_MINUTES


@dataclass(frozen=True)
class BenchPlayer:
    season: int
    epa_per40: float
    family: str = None     # None = Role mein family nahi mili


@dataclass(frozen=True)
class Replacement:
    overall: float
    by_family: dict        # {Family: value}
    bench_players: int     # is season ke bench players

    def for_family(self, family):
        """Family ka replacement; family None ho to overall."""
        return self.by_family.get(family, self.overall)


def in_bench_band(minutes, is_d1):
    """Spec ka bench band: D1 team aur 50-149 regular-season minutes."""
    return is_d1 and BENCH_MIN_MINUTES <= minutes <= BENCH_MAX_MINUTES


def replacement_levels(season, bench_by_season):
    """
    season:          jis season ka replacement chahiye
    bench_by_season: {season: [BenchPlayer]} — s-1, s, s+1 jo bhi mojood hon

    Wapas: Replacement
    """
    current = bench_by_season.get(season) or []
    if not current:
        raise ValueError(f"Season {season} mein koi bench player nahi.")

    # Har season ka apna overall (gap usi season ke overall se nikalta hai)
    overall_of = {
        s: statistics.mean(p.epa_per40 for p in players)
        for s, players in bench_by_season.items() if players
    }
    window = [s for s in (season - 1, season, season + 1) if s in overall_of]

    by_family = {}
    for family in Family:
        diffs = [
            p.epa_per40 - overall_of[s]
            for s in window
            for p in bench_by_season[s]
            if p.family == family
        ]
        if diffs:
            by_family[family] = overall_of[season] + statistics.mean(diffs)

    return Replacement(overall=overall_of[season], by_family=by_family, bench_players=len(current))
