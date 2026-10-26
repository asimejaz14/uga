"""rules.py aur placement.py ke unit tests (database nahi chahiye)."""
from django.test import SimpleTestCase

from analytics.choices import DecidedBy, Family, Group, PlayType, Role
from analytics.role.placement import breaks_guardrail, decide_role
from analytics.role.rules import (
    PlayerFacts, big, blocks_rule, creation_rule, self_creation_rule, shooting_rule, steals_rule,
)


def facts(**kw):
    kw.setdefault("percentiles", {})
    return PlayerFacts(**kw)


class RuleTests(SimpleTestCase):

    def test_creation_floor_general(self):
        self.assertEqual(creation_rule(facts(height=77, lead=0.62)), Role.FLOOR_GENERAL)

    def test_creation_missing_lead_is_floor_general(self):
        self.assertEqual(creation_rule(facts(height=77)), Role.FLOOR_GENERAL)

    def test_creation_tall_is_forward(self):
        self.assertEqual(creation_rule(facts(height=81, lead=0.9)), Role.TRADITIONAL_FORWARD)

    def test_creation_short_secondary_creator(self):
        self.assertEqual(creation_rule(facts(height=74, lead=0.2)), Role.COMBO_GUARD)

    def test_self_creation_boundary_77_is_wing(self):
        # Q-15: "under 6'5"" = < 77, to 77.0 Combo Guard nahi
        self.assertEqual(self_creation_rule(facts(height=77)), Role.WING)
        self.assertEqual(self_creation_rule(facts(height=76.5)), Role.COMBO_GUARD)

    def test_steals_rule_blue_cain(self):
        f = facts(height=77.0, inside=0.0, inside2=0.01)
        self.assertEqual(steals_rule(f), Role.THREE_AND_D_WING)

    def test_steals_rule_interior_big(self):
        f = facts(height=82, inside=0.6, percentiles={PlayType.BLOCKS: 0.9, PlayType.DEF_REBOUNDS: 0.5})
        self.assertEqual(steals_rule(f), Role.UGA_BIG)

    def test_big_picks_by_blocks_vs_rebounds(self):
        self.assertEqual(big(facts(percentiles={PlayType.BLOCKS: 0.5, PlayType.DEF_REBOUNDS: 0.5})), Role.UGA_BIG)
        self.assertEqual(big(facts(percentiles={PlayType.BLOCKS: 0.4, PlayType.DEF_REBOUNDS: 0.5})), Role.TRADITIONAL_BIG)

    def test_blocks_missing_inside_is_uga_big(self):
        self.assertEqual(blocks_rule(facts(height=75)), Role.UGA_BIG)

    def test_shooting_specialist_and_three_and_d(self):
        self.assertEqual(shooting_rule(facts(height=76, three_pa_share=0.65)), Role.THREE_PT_SPECIALIST)
        self.assertEqual(shooting_rule(facts(height=78, three_pa_share=0.4, usage=15, usage_median=19)),
                         Role.THREE_AND_D_WING)

    def test_shooting_guard_when_steals_match(self):
        f = facts(height=74, three_pa_share=0.4, shooting_raw=0.70, percentiles={PlayType.STEALS: 0.66})
        self.assertEqual(shooting_rule(f), Role.GUARD)


class GuardrailTests(SimpleTestCase):

    def test_guardrails(self):
        self.assertTrue(breaks_guardrail(Role.UGA_BIG, 76))
        self.assertFalse(breaks_guardrail(Role.UGA_BIG, 77))
        self.assertTrue(breaks_guardrail(Role.GUARD, 81))
        self.assertFalse(breaks_guardrail(Role.GUARD, 80))
        self.assertFalse(breaks_guardrail(Role.UGA_BIG, None))


class DecideRoleTests(SimpleTestCase):

    def test_spec_example_guard_clear_top_group(self):
        # Spec 2.9: Creation 0.88, Self-creation 0.74 -> farq 0.14 -> Floor General, secondary Wing
        groups = {Group.CREATION: (0.815, 0.88), Group.SELF_CREATION: (0.8, 0.74),
                  Group.STEALS: (0.74, 0.69), Group.BLOCKS: (0.22, 0.22)}
        d = decide_role(groups, facts(height=77, lead=0.62, inside=0.12, inside2=0.30))
        self.assertEqual(d.primary, Role.FLOOR_GENERAL)
        self.assertEqual(d.secondary, Role.WING)
        self.assertEqual(d.family, Family.GUARDS)
        self.assertEqual(d.decided_by, DecidedBy.CLEAR_TOP_GROUP)

    def test_blue_cain_close_call_goes_to_higher_volume(self):
        # Steals 0.836 (3 and D) vs Self-creation 0.746 (Wing): farq 0.09 -> close call.
        # TB1-4 lagu nahi (FG nahi, big nahi, length dono jayez, same family) -> TB5
        groups = {Group.STEALS: (0.836, 0.836), Group.SELF_CREATION: (0.906, 0.746),
                  Group.CREATION: (0.701, 0.657), Group.BLOCKS: (0.311, 0.311)}
        f = facts(height=77.0, lead=0.008, inside=0.0, inside2=0.01, front=0.01)
        d = decide_role(groups, f, three_season={Group.STEALS: 0.8, Group.SELF_CREATION: 0.7})
        self.assertEqual(d.primary, Role.THREE_AND_D_WING)
        self.assertEqual(d.secondary, Role.WING)
        self.assertEqual(d.family, Family.WINGS)
        self.assertEqual(d.decided_by, DecidedBy.TB_HIGHER_VOLUME)

    def test_creator_tiebreaker(self):
        # Creation (FG) aur Self-creation (Combo) close; lead >= 50% -> sirf FG
        groups = {Group.SELF_CREATION: (0.9, 0.90), Group.CREATION: (0.85, 0.85)}
        d = decide_role(groups, facts(height=74, lead=0.7))
        self.assertEqual(d.primary, Role.FLOOR_GENERAL)
        self.assertEqual(d.decided_by, DecidedBy.TB_CREATOR)

    def test_guardrail_drops_big_for_short_player(self):
        groups = {Group.INSIDE: (0.9, 0.95), Group.STEALS: (0.6, 0.60)}
        d = decide_role(groups, facts(height=74, inside=0.1, inside2=0.2))
        self.assertEqual(d.primary, Role.GUARD)
        dropped = [p for p in d.proposals if p.dropped_by_guardrail]
        self.assertEqual(dropped[0].group, Group.INSIDE)
