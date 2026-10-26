"""
Level stage 5-6: surplus -> WAR -> tier (spec 3.7, 3.8, 3.9).

    surplus/40 = EPA/40 - replacement(season, family)
    WAR per 40 = surplus/40 / points per win            (quality; tier isi par)
    WAR        = WAR per 40 x minutes/40 x min(1, minutes/400)   (quality x opportunity)

Blue Cain 2026 (spec): surplus 6.616 / 41.69 = 0.1587 -> x 808/40 x 1.00 = 3.21, Dark Green

Ye file PURE PYTHON hai (D-13).
"""
from analytics.constants import RELIABILITY_MINUTES, TIER_BARS, TIER_BELOW_BARS


def war_per_40(surplus_per40, points_per_win):
    return surplus_per40 / points_per_win


def reliability(minutes):
    """Kam minutes par WAR ko chhota karo: min(1, minutes / 400)."""
    return min(1.0, minutes / RELIABILITY_MINUTES)


def war(war_per40, minutes):
    return war_per40 * minutes / 40 * reliability(minutes)


def tier_for(war_per40):
    """WAR per 40 se rang. Bars oonche se neeche check hote hain."""
    for bar, tier in TIER_BARS:
        if war_per40 >= bar:
            return tier
    return TIER_BELOW_BARS
