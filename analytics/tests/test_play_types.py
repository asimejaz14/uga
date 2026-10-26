"""play_types.py ke unit tests (database nahi chahiye)."""
from django.test import SimpleTestCase

from analytics.choices import PlayType, RulesMode
from analytics.role.play_types import (
    POOLED_FIELDS, play_type_counts, play_type_rates, pool_rows, shrunk_share,
)

NATIONAL = {"rim": 0.40, "mid": 0.25, "three": 0.80}


def row(**values):
    """Khaali (sab 0) row, jis mein sirf diye gaye fields bhare hon."""
    base = {field: 0 for field in POOLED_FIELDS}
    base.update(values)
    return base


class HelperTests(SimpleTestCase):

    def test_shrunk_share_docstring_example(self):
        self.assertAlmostEqual(shrunk_share(2, 2, 0.60), 5 / 7)

    def test_shrunk_share_no_makes_is_national(self):
        self.assertAlmostEqual(shrunk_share(0, 0, 0.60), 0.60)

    def test_pool_rows_applies_weights(self):
        pooled = pool_rows({2026: row(assists=100), 2025: row(assists=80)}, {2026: 1.0, 2025: 0.5})
        self.assertEqual(pooled["assists"], 140)

    def test_pool_rows_missing_season_counts_zero(self):
        pooled = pool_rows({2026: row(assists=100)}, {2026: 1.0, 2025: 0.5})
        self.assertEqual(pooled["assists"], 100)


class CountsAndRatesTests(SimpleTestCase):

    def test_spec_assist_rate_example(self):
        # Spec 2.5: 140 assists / 1,400 possessions = 10.0 per 100
        current = row(assists=140, off_poss=1400, def_poss=1400)
        pooled = pool_rows({2026: current}, {2026: 1.0})
        counts = play_type_counts(pooled, current, NATIONAL, RulesMode.COARSE)
        rates = play_type_rates(counts, pooled, current)
        self.assertAlmostEqual(rates[PlayType.ASSISTS], 10.0)

    def test_defense_uses_def_poss(self):
        current = row(steals=30, off_poss=1500, def_poss=1000)
        pooled = pool_rows({2026: current}, {2026: 1.0})
        rates = play_type_rates(play_type_counts(pooled, current, NATIONAL, RulesMode.COARSE), pooled, current)
        self.assertAlmostEqual(rates[PlayType.STEALS], 3.0)

    def test_threes_split_into_own_and_catch_and_shoot(self):
        current = row(fga_three=100, fgm_three=35, fgm_three_ast=35, off_poss=1000, def_poss=1000)
        pooled = pool_rows({2026: current}, {2026: 1.0})
        counts = play_type_counts(pooled, current, NATIONAL, RulesMode.COARSE)
        a = (35 + 5 * 0.80) / (35 + 5)
        self.assertAlmostEqual(counts[PlayType.CS_THREES], 100 * a)
        self.assertAlmostEqual(counts[PlayType.OWN_THREES] + counts[PlayType.CS_THREES], 100)

    def test_coarse_proxies_exclude_putbacks(self):
        current = row(fga_rim=60, putbacks=10, off_poss=1000, def_poss=1000)
        pooled = pool_rows({2026: current}, {2026: 1.0})
        counts = play_type_counts(pooled, current, NATIONAL, RulesMode.COARSE)
        self.assertAlmostEqual(counts[PlayType.UNAST_RIM] + counts[PlayType.AST_RIM_ATTEMPTS], 50)

    def test_full_mode_without_tagged_games_is_blank(self):
        current = row(off_poss=500, def_poss=500, tagged_off_poss=0, driving_layups=0, pullup_range_2s=7)
        pooled = pool_rows({2026: current}, {2026: 1.0})
        counts = play_type_counts(pooled, current, NATIONAL, RulesMode.FULL)
        rates = play_type_rates(counts, pooled, current)
        self.assertIsNone(rates[PlayType.DRIVING_LAYUPS])     # A-10
        self.assertIsNone(rates[PlayType.CUT_ROLL])
        self.assertAlmostEqual(rates[PlayType.PULLUP_RANGE_2S], 1.4)  # 7/500*100, A-11

    def test_tagged_uses_tagged_possessions_only(self):
        current = row(off_poss=1000, def_poss=1000, tagged_off_poss=600, driving_layups=30)
        pooled = pool_rows({2026: current, 2025: row(off_poss=800)}, {2026: 1.0, 2025: 0.5})
        rates = play_type_rates(play_type_counts(pooled, current, NATIONAL, RulesMode.FULL), pooled, current)
        self.assertAlmostEqual(rates[PlayType.DRIVING_LAYUPS], 5.0)   # 30/600, pool nahi

    def test_no_possessions_gives_none(self):
        current = row()
        pooled = pool_rows({2026: current}, {2026: 1.0})
        rates = play_type_rates(play_type_counts(pooled, current, NATIONAL, RulesMode.COARSE), pooled, current)
        self.assertIsNone(rates[PlayType.ASSISTS])
