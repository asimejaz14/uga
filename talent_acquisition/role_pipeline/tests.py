"""
Unit tests for the Role pipeline steps. No database needed (SimpleTestCase).

    python manage.py test talent_acquisiton.role_pipeline

Each test builds a tiny hand-made DataFrame, so the expected answer can be worked
out on paper. Where the spec gives a worked example, the test uses those numbers.
"""
import math

import numpy as np
import pandas as pd
from django.test import SimpleTestCase

from .assist_share import national_assist_share, shrunk_assisted_share
from .play_types import (build_play_types, build_rates, compute_play_types, percentile_vs,
                         play_types_for)
from .pooling import POOLED_COUNTS, TAGGED_COUNTS, pool_season
from .possessions import count_player_possessions
from .groups import mean_of_top_two
from .placement import place_player
from .rules import Rules
from .shares import compute_shares, rank_in_five

C = {"MIN_POSS": 300, "MIN_PCT_QUALIFIED": 40, "PREV_SEASON_WEIGHT": 0.5, "SHRINK_K": 5}
NATIONAL = {"rim": 0.5, "mid": 0.3, "three": 0.7}


# ---------------------------------------------------------------------------
# helpers to build small inputs
# ---------------------------------------------------------------------------

def poss_row(pid, season, off, de=None, tagged=None, team=1):
    return dict(player_id=pid, season=season, team_id=team, off_poss=off,
                def_poss=off if de is None else de, tagged_off_poss=tagged)


def count_row(pid, season, **kw):
    row = dict(player_id=pid, season=season, team_id=1)
    row.update({c: 0 for c in POOLED_COUNTS})
    row.update({c: np.nan for c in TAGGED_COUNTS})
    row.update(kw)
    return row


def torvik_row(pid, season, min_pct=60, height=78):
    return dict(player_id=pid, season=season, team_id=1, height_in=height,
                min_pct=min_pct, usage=20, three_pa_share=0.3)


def pool(poss, counts, torvik, season=2026):
    return pool_season(pd.DataFrame(poss), pd.DataFrame(counts), pd.DataFrame(torvik),
                       season, C).set_index("player_id")


# ---------------------------------------------------------------------------
# Step 1
# ---------------------------------------------------------------------------

class PossessionTests(SimpleTestCase):
    def setUp(self):
        self.games = pd.DataFrame([
            dict(game_id=1, season=2026, season_type=2, tournament_id=None, has_shot_tags=True),
            dict(game_id=2, season=2026, season_type=2, tournament_id=77, has_shot_tags=False),
        ])

    def _poss(self, game, off, de, garbage=False):
        return dict(game_id=game, possession_no=0, season=2026, off_team_id=1, def_team_id=2,
                    **{f"off_p{i+1}": v for i, v in enumerate(off)},
                    **{f"def_p{i+1}": v for i, v in enumerate(de)}, garbage_time=garbage)

    def test_filters(self):
        a, b = [1, 2, 3, 4, 5], [6, 7, 8, 9, 10]
        poss = pd.DataFrame([
            self._poss(1, a, b),                       # counts
            self._poss(1, a, b, garbage=True),         # garbage time: dropped
            self._poss(2, a, b),                       # tournament game: dropped
            self._poss(1, a, [6, 7, 8, 9, 9]),         # defence duplicate: offence still counts
        ]).astype({f"{s}_p{i}": "Int64" for s in ("off", "def") for i in range(1, 6)})
        out = count_player_possessions(poss, self.games).set_index("player_id")
        self.assertEqual(out.loc[1, "off_poss"], 2)
        self.assertEqual(out.loc[1, "tagged_off_poss"], 2)
        self.assertEqual(out.loc[6, "def_poss"], 1)    # only the clean defence row


# ---------------------------------------------------------------------------
# Step 2
# ---------------------------------------------------------------------------

class AssistShareTests(SimpleTestCase):
    def test_national_share(self):
        counts = pd.DataFrame([
            dict(season=2026, fgm_rim=10, fgm_rim_ast=4, fgm_mid=5, fgm_mid_ast=1,
                 fgm_three=8, fgm_three_ast=6),
            dict(season=2026, fgm_rim=10, fgm_rim_ast=6, fgm_mid=5, fgm_mid_ast=2,
                 fgm_three=2, fgm_three_ast=2),
        ])
        share = national_assist_share(counts).set_index("zone")["ast_share"]
        self.assertAlmostEqual(share["rim"], 10 / 20)
        self.assertAlmostEqual(share["mid"], 3 / 10)
        self.assertAlmostEqual(share["three"], 8 / 10)

    def test_shrink(self):
        # 3 assisted of 4 makes, national 0.60 -> (3 + 3.0) / (4 + 5)
        self.assertAlmostEqual(shrunk_assisted_share(3, 4, 0.60), 6 / 9)
        # no makes at all -> exactly the national share
        self.assertAlmostEqual(shrunk_assisted_share(0, 0, 0.60), 0.60)


# ---------------------------------------------------------------------------
# Step 3
# ---------------------------------------------------------------------------

class PoolingTests(SimpleTestCase):
    def test_established_adds_half_of_last_season(self):
        p = pool([poss_row(1, 2026, 1000), poss_row(1, 2025, 800)],
                 [count_row(1, 2026, assists=100), count_row(1, 2025, assists=60)],
                 [torvik_row(1, 2026)])
        self.assertEqual(p.loc[1, "off_poss"], 1000 + 0.5 * 800)
        self.assertEqual(p.loc[1, "assists"], 100 + 0.5 * 60)
        self.assertEqual(p.loc[1, "confidence"], "normal")
        self.assertTrue(p.loc[1, "read"])
        self.assertTrue(p.loc[1, "qualified"])

    def test_low_minute_adds_all_of_last_season(self):
        p = pool([poss_row(1, 2026, 200), poss_row(1, 2025, 150), poss_row(1, 2024, 500)],
                 [count_row(1, s) for s in (2024, 2025, 2026)], [torvik_row(1, 2026)])
        self.assertEqual(p.loc[1, "off_poss"], 350)        # 2024 not needed
        self.assertEqual(p.loc[1, "confidence"], "low")
        self.assertTrue(p.loc[1, "read"])
        self.assertFalse(p.loc[1, "qualified"])            # qualified uses THIS season only

    def test_low_minute_reaches_back_two_seasons(self):
        p = pool([poss_row(1, 2026, 100), poss_row(1, 2025, 100), poss_row(1, 2024, 150)],
                 [count_row(1, s) for s in (2024, 2025, 2026)], [torvik_row(1, 2026)])
        self.assertEqual(p.loc[1, "off_poss"], 350)
        self.assertEqual(p.loc[1, "seasons_used"], "2026+2025+2024")

    def test_no_read_is_fallback(self):
        p = pool([poss_row(1, 2026, 50)], [count_row(1, 2026)], [torvik_row(1, 2026)])
        self.assertFalse(p.loc[1, "read"])
        self.assertTrue(p.loc[1, "fallback"])

    def test_qualified_needs_minutes_pct(self):
        p = pool([poss_row(1, 2026, 900)], [count_row(1, 2026)], [torvik_row(1, 2026, min_pct=35)])
        self.assertFalse(p.loc[1, "qualified"])

    def test_tagged_counts_are_never_pooled(self):
        p = pool([poss_row(1, 2026, 1000, tagged=600), poss_row(1, 2025, 800)],
                 [count_row(1, 2026, driving_layups=30), count_row(1, 2025)],
                 [torvik_row(1, 2026)])
        self.assertEqual(p.loc[1, "driving_layups"], 30)
        self.assertEqual(p.loc[1, "tagged_off_poss"], 600)


# ---------------------------------------------------------------------------
# Step 4
# ---------------------------------------------------------------------------

class PlayTypeTests(SimpleTestCase):
    def _pooled(self, **kw):
        row = {c: 0.0 for c in POOLED_COUNTS + TAGGED_COUNTS}
        row.update(player_id=1, season=2026, off_poss=1400, def_poss=1400, off_poss_this=1400,
                   tagged_off_poss=np.nan, qualified=True, read=True)
        row.update(kw)
        return pd.DataFrame([row])

    def test_counts_by_mode(self):
        self.assertEqual(len(play_types_for("coarse")), 16)
        self.assertEqual(len(play_types_for("full")), 21)
        self.assertNotIn("alley_oops", play_types_for("full"))

    def test_spec_rate_examples(self):
        # spec 2.5: 140 assists in 1,400 possessions = 10.0 per 100; 70 in 600 = 11.7
        for assists, poss, rate in [(140, 1400, 10.0), (70, 600, 70 / 600 * 100)]:
            p = self._pooled(assists=assists, off_poss=poss)
            r = build_rates(build_play_types(p, NATIONAL, "coarse"), p, "coarse")
            self.assertAlmostEqual(r.loc[0, "assists"], rate)

    def test_defence_uses_defensive_possessions(self):
        p = self._pooled(steals=40, def_poss=1000)
        r = build_rates(build_play_types(p, NATIONAL, "coarse"), p, "coarse")
        self.assertAlmostEqual(r.loc[0, "steals"], 4.0)

    def test_own_vs_catch_and_shoot_threes(self):
        # 100 3PA; 20 makes, 10 assisted; national three 0.7 -> a = (10 + 3.5) / 25 = 0.54
        p = self._pooled(fga_three=100, fgm_three=20, fgm_three_ast=10)
        pt = build_play_types(p, NATIONAL, "coarse")
        self.assertAlmostEqual(pt.loc[0, "cs_threes"], 54.0)
        self.assertAlmostEqual(pt.loc[0, "own_threes"], 46.0)

    def test_coarse_proxies_exclude_putbacks(self):
        # rim FGA 50, putbacks 10 -> 40 non-putback; 0 makes -> a_rim = national 0.5
        p = self._pooled(fga_rim=50, putbacks=10)
        pt = build_play_types(p, NATIONAL, "coarse")
        self.assertAlmostEqual(pt.loc[0, "unassisted_rim"], 20.0)
        self.assertAlmostEqual(pt.loc[0, "assisted_rim"], 20.0)

    def test_tagged_rate_blank_without_tagged_games(self):
        p = self._pooled(driving_layups=5, tagged_off_poss=0)
        r = build_rates(build_play_types(p, NATIONAL, "full"), p, "full")
        self.assertTrue(math.isnan(r.loc[0, "driving_layups"]))

    def test_percentile_is_share_strictly_lower(self):
        ref = pd.Series([1.0, 2.0, 3.0, 4.0])
        got = percentile_vs(pd.Series([3.0, 0.5, 9.0, np.nan]), ref)
        self.assertEqual(list(got[:3]), [0.5, 0.0, 1.0])
        self.assertTrue(math.isnan(got[3]))

    def test_percentile_against_qualified_only(self):
        # player 3 is not qualified: his huge rate must not push the others down
        p = pd.concat([self._pooled(player_id=i, assists=a, qualified=q)
                       for i, a, q in [(1, 100, True), (2, 200, True), (3, 900, False)]],
                      ignore_index=True)
        out = compute_play_types(p, NATIONAL, "coarse").set_index("player_id")
        self.assertEqual(out.loc[1, "pctl_assists"], 0.0)
        self.assertEqual(out.loc[2, "pctl_assists"], 0.5)
        self.assertEqual(out.loc[3, "pctl_assists"], 1.0)


# ---------------------------------------------------------------------------
# Step 5
# ---------------------------------------------------------------------------

class ShareTests(SimpleTestCase):
    def test_rank_in_five(self):
        # rank = 1 + how many of the other four are strictly higher
        ranks = rank_in_five(np.array([[10.0, 4.0, 7.0, 4.0, 2.0]]))
        self.assertEqual(ranks.tolist(), [[1, 3, 2, 3, 5]])

    def _inputs(self, lineups, assists, reads=None, heights=None):
        """Build the four inputs compute_shares needs from plain lists/dicts."""
        games = pd.DataFrame([dict(game_id=1, season=2026, season_type=2,
                                   tournament_id=None, has_shot_tags=False)])
        poss = pd.DataFrame([
            dict(game_id=1, possession_no=i, season=2026, off_team_id=1, def_team_id=2,
                 **{f"off_p{j+1}": p for j, p in enumerate(five)},
                 **{f"def_p{j+1}": 90 + j for j in range(5)}, garbage_time=False)
            for i, five in enumerate(lineups)
        ]).astype({f"{s}_p{i}": "Int64" for s in ("off", "def") for i in range(1, 6)})
        ids = sorted({p for five in lineups for p in five})
        reads = reads or {p: True for p in ids}
        heights = heights or {p: 70 + p for p in ids}
        pt = pd.DataFrame([dict(player_id=p, rate_assists=assists[p], rate_orb=0.0,
                                rate_blocks=0.0, rate_putbacks=float(p)) for p in ids])
        pooled = pd.DataFrame([dict(player_id=p, read=reads[p], height_in=heights[p]) for p in ids])
        return poss, games, pt, pooled

    def test_lead_changes_with_teammates(self):
        # Player 1 (assists 8) is the best passer with 2-5, but not when 6 (assists 12) plays.
        lineups = [[1, 2, 3, 4, 5]] * 3 + [[1, 6, 3, 4, 5]]
        assists = {1: 8.0, 2: 3.0, 3: 2.0, 4: 1.0, 5: 0.5, 6: 12.0}
        out = compute_shares(*self._inputs(lineups, assists), 2026, min_poss=1).set_index("player_id")
        self.assertAlmostEqual(out.loc[1, "lead"], 3 / 4)    # #1 in 3 of his 4 possessions
        self.assertAlmostEqual(out.loc[1, "lead2"], 1.0)     # always top two
        self.assertAlmostEqual(out.loc[6, "lead"], 1.0)

    def test_front_is_two_tallest(self):
        lineups = [[1, 2, 3, 4, 5]]
        out = compute_shares(*self._inputs(lineups, {p: 1.0 for p in range(1, 6)}), 2026,
                             min_poss=1).set_index("player_id")
        # heights are 71..75, so players 4 and 5 are the two tallest
        self.assertEqual(out["front"].tolist(), [0.0, 0.0, 0.0, 1.0, 1.0])

    def test_possession_needs_four_reads(self):
        lineups = [[1, 2, 3, 4, 5]]
        reads = {1: True, 2: True, 3: True, 4: False, 5: False}      # only 3 reads
        out = compute_shares(*self._inputs(lineups, {p: 1.0 for p in range(1, 6)}, reads), 2026,
                             min_poss=1)
        self.assertTrue(out.empty)

    def test_player_without_read_is_ranked_last(self):
        lineups = [[1, 2, 3, 4, 5]]
        reads = {1: False, 2: True, 3: True, 4: True, 5: True}       # 4 reads: counts
        assists = {1: 50.0, 2: 3.0, 3: 2.0, 4: 1.0, 5: 0.5}            # 1 would be #1 ...
        out = compute_shares(*self._inputs(lineups, assists, reads), 2026,
                             min_poss=1).set_index("player_id")
        self.assertEqual(out.loc[1, "lead"], 0.0)                    # ... but has no read
        self.assertEqual(out.loc[2, "lead"], 1.0)

    def test_under_min_possessions_is_missing(self):
        lineups = [[1, 2, 3, 4, 5]] * 3
        out = compute_shares(*self._inputs(lineups, {p: float(p) for p in range(1, 6)}), 2026,
                             min_poss=200)
        self.assertTrue(out["lead"].isna().all())
        self.assertEqual(out["valid_poss"].tolist(), [3] * 5)


# ---------------------------------------------------------------------------
# Steps 6-8
# ---------------------------------------------------------------------------

RULE_C = {"H_WING": 77, "H_67": 79, "H_GUARD_MAX": 80, "SHARE_THRESHOLD": 0.50,
          "THREE_SHARE_SPEC": 0.60, "DRB_PCTL_HIGH": 0.60, "DRB_PCTL_LOW": 0.50,
          "STEAL_SHOOT_MARGIN": 0.05, "DEF_CLOSE": 0.10}
NAN = float("nan")


def spec_guard(**changes):
    """The invented guard from spec 2.9 (6'5", lead 62%, inside 12% ...)."""
    p = dict(height_in=77, lead=0.62, lead2=0.85, inside=0.12, inside2=0.30, front=0.08,
             pctl_drb=0.40, pctl_blocks=0.22, pctl_steals=0.74,
             three_pa_share=0.30, usage=22, usage_median=20, raw_shooting=0.30)
    p.update(changes)
    return p


def cands(*pairs):
    """('Wing', 0.8), ('Guard', 0.75) -> proposal dicts; group names are just labels."""
    return [{"group": f"g{i}", "role": r, "score": s} for i, (r, s) in enumerate(pairs)]


class GroupTests(SimpleTestCase):
    def test_mean_of_top_two(self):
        df = pd.DataFrame([[0.85, 0.78, 0.60], [0.40, NAN, NAN], [NAN, NAN, NAN]])
        got = mean_of_top_two(df)
        self.assertAlmostEqual(got[0], 0.815)          # spec 2.7 Creation example
        self.assertAlmostEqual(got[1], 0.40)
        self.assertTrue(math.isnan(got[2]))


class RuleTests(SimpleTestCase):
    def test_spec_example_proposals(self):
        roles = Rules(RULE_C).propose_all(spec_guard())
        self.assertEqual(roles["creation"], "Floor General")     # lead 62% >= 50%
        self.assertEqual(roles["self_creation"], "Wing")         # 6'5", not 6'8"+
        self.assertEqual(roles["steals"], "3 and D Wing")        # not interior, 6'5"+
        self.assertEqual(roles["def_glass"], "Traditional Forward")
        self.assertEqual(roles["inside"], "Traditional Big")     # blocks 0.22 < drb 0.40

    def test_creator_beside_better_passer_under_65(self):
        roles = Rules(RULE_C).propose_all(spec_guard(height_in=74, lead=0.20))
        self.assertEqual(roles["creation"], "Combo Guard")

    def test_missing_lead_counts_as_floor_general(self):
        roles = Rules(RULE_C).propose_all(spec_guard(lead=NAN))
        self.assertEqual(roles["creation"], "Floor General")

    def test_shooting_specialist_by_three_share(self):
        roles = Rules(RULE_C).propose_all(spec_guard(three_pa_share=0.65))
        self.assertEqual(roles["shooting"], "3pt Specialist")


class PlacementTests(SimpleTestCase):
    def test_spec_example_end_to_end(self):
        # spec 2.9: Creation 0.88 ... Blocks 0.22 -> Floor General / Wing / clear
        scores = dict(creation=0.88, self_creation=0.74, steals=0.69, def_glass=0.40,
                      inside=0.35, shooting=0.31, blocks=0.22)
        p = spec_guard()
        roles = Rules(RULE_C).propose_all(p)
        proposals = [{"group": g, "role": roles[g], "score": s} for g, s in scores.items()]
        out = place_player(proposals, p, None, RULE_C)
        self.assertEqual(out["primary"], "Floor General")
        self.assertEqual(out["secondary"], "Wing")
        self.assertEqual(out["decided_by"], "clear")             # 0.88 - 0.74 = 0.14 > 0.10

    def test_guardrail_drops_short_big(self):
        out = place_player(cands(("UGA Big", 0.9), ("Guard", 0.5)),
                           spec_guard(height_in=75), None, RULE_C)
        self.assertEqual(out["primary"], "Guard")

    def test_creator_tiebreaker(self):
        # close call (0.05 apart); lead 40% < 50% removes the Floor General
        out = place_player(cands(("Floor General", 0.80), ("Combo Guard", 0.75)),
                           spec_guard(height_in=74, lead=0.40), None, RULE_C)
        self.assertEqual((out["primary"], out["decided_by"]), ("Combo Guard", "creator"))

    def test_length_tiebreaker(self):
        # 6'3": a wing role is not allowed to win a close call
        out = place_player(cands(("Wing", 0.80), ("Guard", 0.75)),
                           spec_guard(height_in=75, lead=NAN), None, RULE_C)
        self.assertEqual((out["primary"], out["decided_by"]), ("Guard", "length"))

    def test_volume_is_last_resort(self):
        p = spec_guard(height_in=NAN, lead=NAN, inside=NAN)
        out = place_player(cands(("Combo Guard", 0.80), ("Guard", 0.75)), p, None, RULE_C)
        self.assertEqual((out["primary"], out["decided_by"]), ("Combo Guard", "volume"))

    def test_larger_sample_needs_different_families(self):
        p = spec_guard(height_in=NAN, lead=NAN, inside=NAN)
        three = {"g0": 0.2, "g1": 0.9}           # 3-season sample prefers the 2nd one
        out = place_player(cands(("Combo Guard", 0.80), ("Wing", 0.75)), p, three, RULE_C)
        self.assertEqual((out["primary"], out["decided_by"]), ("Wing", "larger_sample"))
