"""shares.py ke unit tests (database nahi chahiye)."""
from django.test import SimpleTestCase

from analytics.role.shares import compute_shares, rank_within

ALL_READ = {1, 2, 3, 4, 5, 6}
HEIGHTS = {1: 72, 2: 75, 3: 78, 4: 81, 5: 84, 6: 76}


class RankTests(SimpleTestCase):

    def test_docstring_example(self):
        self.assertEqual(rank_within(["A", "B", "C"], {"A": 5, "B": 9, "C": 5}), {"B": 1, "A": 2, "C": 2})


class ComputeSharesTests(SimpleTestCase):

    def setUp(self):
        # Player 1 sab se bara passer, player 5 sab se bara interior aur sab se lamba
        self.assists = {1: 10, 2: 6, 3: 4, 4: 2, 5: 1, 6: 8}
        self.interior = {1: 1, 2: 2, 3: 3, 4: 6, 5: 9, 6: 2}

    def test_basic_shares(self):
        lineups = {(1, 2, 3, 4, 5): 300}
        shares, totals = compute_shares(lineups, self.assists, self.interior, ALL_READ, HEIGHTS)
        self.assertEqual(shares[1].lead, 1.0)
        self.assertEqual(shares[2].lead, 0.0)
        self.assertEqual(shares[2].lead2, 1.0)
        self.assertEqual(shares[5].inside, 1.0)
        self.assertEqual(shares[4].inside2, 1.0)
        self.assertEqual(shares[5].front, 1.0)   # 84 sab se lamba
        self.assertEqual(shares[4].front, 1.0)   # 81 doosra
        self.assertEqual(shares[3].front, 0.0)
        self.assertEqual(totals["lead_firsts"], 300)

    def test_share_is_fraction_of_possessions(self):
        # 1 aur 6 kabhi saath nahi: 300 possessions mein 6 lead hai, 100 mein 2 ke saath 1
        lineups = {(1, 2, 3, 4, 5): 100, (2, 3, 4, 5, 6): 300}
        shares, _ = compute_shares(lineups, self.assists, self.interior, ALL_READ, HEIGHTS)
        self.assertAlmostEqual(shares[2].lead, 0.0)
        self.assertAlmostEqual(shares[2].lead2, 1.0)        # 100 (1 ke baad) + 300 (6 ke baad)
        self.assertAlmostEqual(shares[6].lead, 1.0)

    def test_possession_skipped_when_fewer_than_four_reads(self):
        lineups = {(1, 2, 3, 4, 5): 300}
        shares, totals = compute_shares(lineups, self.assists, self.interior, {1, 2, 3}, HEIGHTS)
        self.assertEqual(shares, {})
        self.assertEqual(totals["valid_possessions"], 0)

    def test_player_without_read_gets_no_shares_and_is_not_ranked(self):
        # 1 ka read nahi -> ranking 2..5 mein, to 2 lead banta hai
        lineups = {(1, 2, 3, 4, 5): 300}
        shares, _ = compute_shares(lineups, self.assists, self.interior, {2, 3, 4, 5}, HEIGHTS)
        self.assertNotIn(1, shares)
        self.assertEqual(shares[2].lead, 1.0)

    def test_under_200_possessions_is_null(self):
        lineups = {(1, 2, 3, 4, 5): 199}
        shares, _ = compute_shares(lineups, self.assists, self.interior, ALL_READ, HEIGHTS)
        self.assertEqual(shares[1].valid_poss, 199)
        self.assertIsNone(shares[1].lead)

    def test_missing_height_gives_null_front(self):
        lineups = {(1, 2, 3, 4, 5): 300}
        heights = {k: v for k, v in HEIGHTS.items() if k != 5}
        shares, _ = compute_shares(lineups, self.assists, self.interior, ALL_READ, heights)
        self.assertIsNone(shares[5].front)
        self.assertEqual(shares[3].front, 1.0)   # 5 ke baghair 3 doosra lamba (78)

    def test_tied_assist_rates_share_rank_one(self):
        assists = {1: 5, 2: 5, 3: 1, 4: 1, 5: 1}
        lineups = {(1, 2, 3, 4, 5): 300}
        shares, totals = compute_shares(lineups, assists, self.interior, ALL_READ, HEIGHTS)
        self.assertEqual(shares[1].lead, 1.0)
        self.assertEqual(shares[2].lead, 1.0)
        self.assertEqual(totals["lead_firsts"], 600)   # isi liye ratio 1.0 se upar ja sakta hai
