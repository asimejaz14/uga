"""percentiles.py ke unit tests (database nahi chahiye)."""
from django.test import SimpleTestCase

from analytics.role.percentiles import (
    group_raw_score, group_scores, percentile_of, play_type_percentiles, top_play_types,
)


class PercentileOfTests(SimpleTestCase):

    def test_docstring_examples(self):
        population = [2, 4, 6, 8]
        self.assertEqual(percentile_of(6, population), 0.50)
        self.assertEqual(percentile_of(7, population), 0.75)

    def test_ties_are_not_counted_as_lower(self):
        # A-18: barabar wale "lower" nahi
        self.assertEqual(percentile_of(4, [4, 4, 4, 8]), 0.0)

    def test_lowest_and_above_highest(self):
        self.assertEqual(percentile_of(1, [2, 4]), 0.0)
        self.assertEqual(percentile_of(9, [2, 4]), 1.0)

    def test_none(self):
        self.assertIsNone(percentile_of(None, [1, 2]))
        self.assertIsNone(percentile_of(3, []))


class PlayTypePercentileTests(SimpleTestCase):

    def test_population_is_qualified_only(self):
        rates = {1: {"a": 2}, 2: {"a": 4}, 3: {"a": 100}}    # 3 qualified nahi
        pcts = play_type_percentiles(rates, qualified_ids={1, 2}, play_types=["a"])
        self.assertEqual(pcts[2]["a"], 0.5)                    # 100 wala population mein nahi
        self.assertEqual(pcts[3]["a"], 1.0)                    # non-qualified ko bhi percentile milta hai


class GroupScoreTests(SimpleTestCase):

    def test_spec_creation_example_raw(self):
        # Spec 2.7 Stage B: 0.85, 0.78, 0.60 -> 0.815
        pcts = {"assists": 0.85, "ast_rim": 0.78, "ast_three": 0.60}
        self.assertAlmostEqual(group_raw_score(pcts, ["assists", "ast_rim", "ast_three"]), 0.815)

    def test_one_member_present(self):
        self.assertEqual(group_raw_score({"a": 0.4, "b": None}, ["a", "b"]), 0.4)

    def test_none_present(self):
        self.assertIsNone(group_raw_score({"a": None}, ["a"]))

    def test_group_score_is_percentile_of_raw(self):
        percentiles = {1: {"a": 0.1}, 2: {"a": 0.5}, 3: {"a": 0.9}}
        scores = group_scores(percentiles, qualified_ids={1, 2, 3}, groups={"g": ["a"]})
        self.assertEqual(scores[3]["g"], (0.9, 2 / 3))

    def test_top_play_types(self):
        top = top_play_types({"a": 0.9, "b": None, "c": 0.95, "d": 0.1, "e": 0.5, "f": 0.6})
        self.assertEqual([t["play_type"] for t in top], ["c", "a", "f", "e"])
