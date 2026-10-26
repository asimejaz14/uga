"""
pooling.py ke unit tests (database nahi chahiye).

    python manage.py test analytics
"""
from django.test import SimpleTestCase

from analytics.choices import Confidence
from analytics.role.pooling import (
    ESTABLISHED, FALLBACK, NO_DATA, POOLED, POOLED_THREE, decide_pooling,
)

ALL_SEASONS = {2024, 2025, 2026}


class DecidePoolingTests(SimpleTestCase):

    def test_established_uses_half_of_last_season(self):
        r = decide_pooling(1, 2026, {2026: 1436, 2025: 1000}, ALL_SEASONS)
        self.assertEqual(r.status, ESTABLISHED)
        self.assertEqual(r.weights, {2026: 1.0, 2025: 0.5})
        self.assertEqual(r.pooled_off_poss, 1436 + 500)
        self.assertEqual(r.confidence, Confidence.NORMAL)
        self.assertFalse(r.fallback)
        self.assertTrue(r.has_read)

    def test_exactly_300_is_established(self):
        self.assertEqual(decide_pooling(1, 2026, {2026: 300}, ALL_SEASONS).status, ESTABLISHED)

    def test_low_minute_pooled_with_full_last_season(self):
        r = decide_pooling(1, 2026, {2026: 120, 2025: 200}, ALL_SEASONS)
        self.assertEqual(r.status, POOLED)
        self.assertEqual(r.pooled_off_poss, 320)
        self.assertEqual(r.confidence, Confidence.LOW)
        self.assertFalse(r.fallback)

    def test_needs_third_season(self):
        r = decide_pooling(1, 2026, {2026: 100, 2025: 100, 2024: 150}, ALL_SEASONS)
        self.assertEqual(r.status, POOLED_THREE)
        self.assertEqual(r.weights, {2026: 1.0, 2025: 1.0, 2024: 1.0})
        self.assertEqual(r.pooled_off_poss, 350)

    def test_fallback_when_still_short(self):
        r = decide_pooling(1, 2026, {2026: 50, 2025: 40}, ALL_SEASONS)
        self.assertEqual(r.status, FALLBACK)
        self.assertTrue(r.fallback)
        self.assertFalse(r.has_read)

    def test_no_data(self):
        r = decide_pooling(1, 2026, {}, ALL_SEASONS)
        self.assertEqual(r.status, NO_DATA)
        self.assertTrue(r.fallback)

    def test_history_incomplete_when_last_season_missing_from_database(self):
        # 2024 ka established player: rule 2023 maangta hai, jo data mein nahi
        r = decide_pooling(1, 2024, {2024: 900}, ALL_SEASONS)
        self.assertEqual(r.status, ESTABLISHED)
        self.assertFalse(r.history_complete)

    def test_player_absent_last_season_is_still_complete(self):
        # Freshman: 2025 mein khela hi nahi, lekin 2025 ka data database mein hai
        r = decide_pooling(1, 2026, {2026: 900}, ALL_SEASONS)
        self.assertTrue(r.history_complete)
