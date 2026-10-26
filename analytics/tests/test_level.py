"""Level ke pure functions ke tests (database nahi chahiye)."""
from django.test import SimpleTestCase

from analytics.choices import Tier
from analytics.level.epa import PIECES, coverage, epa_pieces, per_40
from analytics.level.league import LeagueValues
from analytics.level.replacement import BenchPlayer, in_bench_band, replacement_levels
from analytics.level.war import reliability, tier_for, war, war_per_40

LEAGUE = LeagueValues(
    league_ft_pct=0.72,
    fg_pct={"rim": 0.6, "mid": 0.38, "three": 0.34},
    xpts={"rim": 1.3100, "mid": 0.9548, "three": 1.2139},
    national_share={"rim": 0.42, "mid": 0.26, "three": 0.83},
    ast_share_jumper=0.61,
)
ZERO = {k: 0 for k in (
    "fga_rim", "fgm_rim", "fgm_rim_ast", "fga_mid", "fgm_mid", "fgm_mid_ast",
    "fga_three", "fgm_three", "fgm_three_ast", "fta", "ftm", "assists", "ast_to_rim",
    "ast_to_three", "turnovers", "orb", "steals", "blocks", "fts_conceded", "technicals")}


def counts(**kw):
    return {**ZERO, **kw}


class EpaTests(SimpleTestCase):

    def test_spec_mini_ledger_values(self):
        # Spec ke example: unassisted rim make +0.925, assisted three (shooter) +1.786
        p = epa_pieces(counts(fga_rim=1, fgm_rim=1), LEAGUE)
        self.assertAlmostEqual(p["epa_self_creation"], 0.925)
        p = epa_pieces(counts(fga_three=1, fgm_three=1, fgm_three_ast=1), LEAGUE)
        self.assertAlmostEqual(p["epa_shooting"], 3 - 1.2139)

    def test_assist_to_rim_credit(self):
        p = epa_pieces(counts(assists=1, ast_to_rim=1), LEAGUE)
        self.assertAlmostEqual(p["epa_creation"], 1.3100 - 1.075)

    def test_mid_range_assist_is_negative(self):
        p = epa_pieces(counts(assists=1), LEAGUE)
        self.assertAlmostEqual(p["epa_creation"], 0.9548 - 1.075)

    def test_miss_split_adds_to_minus_0774(self):
        p = epa_pieces(counts(fga_mid=1), LEAGUE)
        self.assertAlmostEqual(p["epa_self_creation"] + p["epa_shooting"], -0.774)

    def test_free_throws_drawing_plus_making(self):
        # 2 made, 1 missed: 2*0.53 - 0.47 = 0.59
        p = epa_pieces(counts(fta=3, ftm=2), LEAGUE)
        self.assertAlmostEqual(p["epa_ft_drawing"] + p["epa_ft_making"], 0.59)
        self.assertAlmostEqual(p["epa_ft_drawing"], 3 * (0.72 - 0.47))

    def test_other_events(self):
        p = epa_pieces(counts(turnovers=1, orb=1, steals=1, blocks=1, fts_conceded=2, technicals=1), LEAGUE)
        self.assertAlmostEqual(p["epa_ball_security"], -1.075)
        self.assertAlmostEqual(p["epa_off_rebounds"], 0.785)
        self.assertAlmostEqual(p["epa_steals"], 1.075)
        self.assertAlmostEqual(p["epa_blocks"], 0.750)
        self.assertAlmostEqual(p["epa_discipline"], -2 * 0.72 - 2 * 0.72)

    def test_eleven_pieces(self):
        self.assertEqual(set(epa_pieces(counts(), LEAGUE)), set(PIECES))

    def test_coverage_and_per40(self):
        self.assertAlmostEqual(coverage(counts(fgm_rim=10, ftm=4), 25), 24 / 25)
        self.assertIsNone(coverage(counts(), 0))
        self.assertAlmostEqual(per_40(100.631, 808), 4.9817, places=4)


class ReplacementTests(SimpleTestCase):

    def test_band(self):
        self.assertTrue(in_bench_band(50, True))
        self.assertTrue(in_bench_band(149, True))
        self.assertFalse(in_bench_band(150, True))
        self.assertFalse(in_bench_band(100, False))

    def test_overall_plus_pooled_family_gap(self):
        bench = {
            2025: [BenchPlayer(2025, -2.0, "guards"), BenchPlayer(2025, 0.0, "bigs")],   # overall -1
            2026: [BenchPlayer(2026, -3.0, "guards"), BenchPlayer(2026, -1.0, "bigs")],  # overall -2
        }
        r = replacement_levels(2026, bench)
        self.assertAlmostEqual(r.overall, -2.0)
        # guards ke farq: 2025: -2-(-1) = -1 ; 2026: -3-(-2) = -1 -> gap -1
        self.assertAlmostEqual(r.for_family("guards"), -3.0)
        self.assertAlmostEqual(r.for_family("bigs"), -1.0)
        self.assertAlmostEqual(r.for_family(None), -2.0)
        self.assertEqual(r.bench_players, 2)


class WarTests(SimpleTestCase):

    def test_blue_cain_spec_chain(self):
        w40 = war_per_40(6.616, 41.69)
        self.assertAlmostEqual(w40, 0.1587, places=4)
        self.assertAlmostEqual(war(w40, 808), 3.21, places=2)
        self.assertEqual(tier_for(w40), Tier.DARK_GREEN)

    def test_reliability_and_tiers(self):
        self.assertEqual(reliability(200), 0.5)
        self.assertEqual(reliability(900), 1.0)
        self.assertEqual(tier_for(0.0913), Tier.LIGHT_GREEN)
        self.assertEqual(tier_for(0.0340), Tier.YELLOW)
        self.assertEqual(tier_for(0.0339), Tier.RED)
