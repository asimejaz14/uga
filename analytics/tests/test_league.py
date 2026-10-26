"""
league.py ke unit tests. Database nahi chahiye (SimpleTestCase).

    python manage.py test analytics
"""
from django.test import SimpleTestCase

from analytics.constants import MISS_VALUE
from analytics.level.league import (
    LeagueShotTotals, TeamRecord, expected_points, fit_points_per_win,
    jumper_share, league_values,
)


class ExpectedPointsTests(SimpleTestCase):

    def test_rim_example_from_docstring(self):
        # 2 * 0.60 + 0.40 * 0.28 * 1.075 = 1.2 + 0.1204
        self.assertAlmostEqual(expected_points(2, 0.60), 1.3204, places=6)

    def test_zero_fg_pct_is_just_rebound_value(self):
        # Kabhi make nahi: sirf 28% ball wapas aane ki qeemat
        self.assertAlmostEqual(expected_points(3, 0.0), 0.301, places=6)

    def test_miss_value_constant(self):
        self.assertAlmostEqual(MISS_VALUE, -0.774, places=6)


class LeagueValuesTests(SimpleTestCase):

    def setUp(self):
        self.totals = LeagueShotTotals(
            fga_rim=1000, fgm_rim=600,
            fga_mid=1000, fgm_mid=400,
            fga_three=1000, fgm_three=350,
            fta=1000, ftm=720,
        )
        self.shares = {"rim": 0.40, "mid": 0.20, "three": 0.80}

    def test_fg_pct_and_ft_pct(self):
        values = league_values(self.totals, self.shares)
        self.assertAlmostEqual(values.fg_pct["rim"], 0.60)
        self.assertAlmostEqual(values.fg_pct["three"], 0.35)
        self.assertAlmostEqual(values.league_ft_pct, 0.72)

    def test_jumper_share_is_make_weighted(self):
        # (0.20 * 400 + 0.80 * 350) / 750 = 360 / 750 = 0.48
        self.assertAlmostEqual(jumper_share(self.shares, 400, 350), 0.48)

    def test_missing_zone_raises(self):
        with self.assertRaises(ValueError):
            league_values(self.totals, {"rim": 0.4, "mid": 0.2})


class PointsPerWinTests(SimpleTestCase):

    def test_recovers_known_line(self):
        # Har team ke liye y = 15 + 0.025 * x  -> points per win = 40
        records = []
        for i, margin_per_game in enumerate([-10, -5, 0, 5, 10]):
            games = 31
            x = margin_per_game * 31
            wins = 15 + 0.025 * x          # y per 31 games = wins (games = 31)
            records.append(TeamRecord(team_id=i, games=games, wins=wins, point_margin=margin_per_game * games))
        fit = fit_points_per_win(records)
        self.assertAlmostEqual(fit.slope, 0.025)
        self.assertAlmostEqual(fit.intercept, 15)
        self.assertAlmostEqual(fit.points_per_win, 40)
        self.assertAlmostEqual(fit.r, 1.0)

    def test_teams_under_ten_games_are_dropped(self):
        records = [
            TeamRecord(1, 20, 15, 100),
            TeamRecord(2, 20, 5, -100),
            TeamRecord(3, 9, 9, 300),      # 9 games: bahar
        ]
        self.assertEqual(fit_points_per_win(records).teams, 2)
