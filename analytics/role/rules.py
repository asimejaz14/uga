"""
Role step R7: har group apna role PROPOSE karta hai (spec 2.7 Stage C).

Har group ka rule ek ORDERED list hai: pehli sharat jo sach ho, wahi
jeetti hai aur aage nahi dekha jata. Har function neeche spec ki table
ki line by line copy hai.

Missing data ka rule:
    - Koi share (lead, inside...) missing ho to jo sharat us share ko use
      karti hai woh SKIP (false) hoti hai — spec: "every rule that uses it
      is skipped". Do jagah spec khud kehta hai "or the share is missing",
      wahan missing ko SACH maana jata hai (Creation line 2, Blocks line 1).
    - Height missing ho to height wali har sharat false (A-24).

Ye file PURE PYTHON hai (D-13).
"""
from dataclasses import dataclass

from analytics.choices import Group, PlayType, Role
from analytics.constants import (
    GUARD_STEALS_MARGIN, H_6_5, H_6_7, H_6_8, SHARE_MAJORITY,
    SHOOTING_DREB_PCT_HIGH, SHOOTING_DREB_PCT_LOW, THREE_SPECIALIST_SHARE,
)


@dataclass(frozen=True)
class PlayerFacts:
    """Rules ko ek player ke baare mein jo kuch chahiye."""
    height: float = None           # inches; None = pata nahi
    lead: float = None             # R6 shares (0-1) ya None
    inside: float = None
    inside2: float = None
    front: float = None
    percentiles: dict = None       # {PlayType: percentile}  R4
    shooting_raw: float = None     # Shooting group ka raw score  R5
    usage: float = None            # Torvik usage
    usage_median: float = None     # qualified players ka usage median
    three_pa_share: float = None   # Torvik (0-1)

    def pct(self, play_type):
        """Play-type percentile; missing ho to 0 (sab se neeche)."""
        return (self.percentiles or {}).get(play_type) or 0.0


# ---------------------------------------------------------------------------
# Chhote helpers: None ko hamesha "false" maante hain
# ---------------------------------------------------------------------------

def under(height, inches):
    """height < inches (height pata ho to)."""
    return height is not None and height < inches


def at_least(height, inches):
    """height >= inches (height pata ho to)."""
    return height is not None and height >= inches


def taller_than(height, inches):
    """height > inches (height pata ho to)."""
    return height is not None and height > inches


def majority(share):
    """Share 50%+ hai (missing ho to false)."""
    return share is not None and share >= SHARE_MAJORITY


def big(f):
    """
    big(): UGA Big ya Traditional Big.
    Blocks percentile >= defensive-rebound percentile -> UGA Big, warna Traditional Big.
    """
    if f.pct(PlayType.BLOCKS) >= f.pct(PlayType.DEF_REBOUNDS):
        return Role.UGA_BIG
    return Role.TRADITIONAL_BIG


# ---------------------------------------------------------------------------
# 7 group rules (spec 2.7 Stage C table, order mein)
# ---------------------------------------------------------------------------

def creation_rule(f):
    if taller_than(f.height, H_6_8):
        return Role.TRADITIONAL_FORWARD          # creator at the big position
    if f.lead is None or majority(f.lead):
        return Role.FLOOR_GENERAL                # best passer of the five (ya share missing)
    if under(f.height, H_6_5):
        return Role.COMBO_GUARD                  # better creator floor par hai
    if majority(f.inside2):
        return Role.TRADITIONAL_FORWARD          # top-two interior
    return Role.WING


def self_creation_rule(f):
    if under(f.height, H_6_5):
        return Role.COMBO_GUARD
    if at_least(f.height, H_6_8) and majority(f.inside2):
        return Role.TRADITIONAL_FORWARD
    return Role.WING


def shooting_rule(f):
    dreb = f.pct(PlayType.DEF_REBOUNDS)
    if (at_least(f.height, H_6_7) and dreb >= SHOOTING_DREB_PCT_HIGH
            and (at_least(f.height, H_6_8) or majority(f.front))):
        return Role.TRADITIONAL_FORWARD          # Stretch 4
    if at_least(f.height, H_6_7) and dreb >= SHOOTING_DREB_PCT_LOW and majority(f.front):
        return Role.TRADITIONAL_FORWARD          # borderline rebounder, lineup decides
    if f.three_pa_share is not None and f.three_pa_share >= THREE_SPECIALIST_SHARE:
        return Role.THREE_PT_SPECIALIST
    if (at_least(f.height, H_6_5) and f.usage is not None and f.usage_median is not None
            and f.usage < f.usage_median):
        return Role.THREE_AND_D_WING
    if (under(f.height, H_6_5) and f.shooting_raw is not None
            and f.pct(PlayType.STEALS) >= f.shooting_raw - GUARD_STEALS_MARGIN):
        return Role.GUARD
    return Role.THREE_PT_SPECIALIST


def steals_rule(f):
    if majority(f.inside):
        return big(f) if at_least(f.height, H_6_8) else Role.TRADITIONAL_FORWARD
    if majority(f.inside2) and at_least(f.height, H_6_5):
        return Role.TRADITIONAL_FORWARD
    if at_least(f.height, H_6_5):
        return Role.THREE_AND_D_WING
    return Role.GUARD


def defensive_glass_rule(f):
    if majority(f.inside):
        return big(f)
    return Role.TRADITIONAL_FORWARD


def blocks_rule(f):
    if f.inside is None or majority(f.inside):
        return Role.UGA_BIG                      # interior player (ya share missing)
    if majority(f.inside2):
        return Role.TRADITIONAL_FORWARD          # shot-blocker beside a bigger interior player
    if at_least(f.height, H_6_5):
        return Role.THREE_AND_D_WING
    return Role.GUARD


def inside_rule(f):
    return big(f)


GROUP_RULES = {
    Group.CREATION: creation_rule,
    Group.SELF_CREATION: self_creation_rule,
    Group.SHOOTING: shooting_rule,
    Group.STEALS: steals_rule,
    Group.DEFENSIVE_GLASS: defensive_glass_rule,
    Group.BLOCKS: blocks_rule,
    Group.INSIDE: inside_rule,
}


def propose_role(group, facts):
    """Ek group ka proposed role."""
    return GROUP_RULES[group](facts)
