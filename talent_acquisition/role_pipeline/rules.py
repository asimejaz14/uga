"""
Step 6b — each group proposes one role (spec 2.7, Stage C).

Every group has an ORDERED list of conditions. The first condition that is true
decides the role, and checking stops. That is exactly an if / elif / else chain,
so that is how each rule is written below — one small method per group, top to
bottom in the same order as the spec table.

Heights (inches)
    6'5" = 77   (H_WING: wing length, and the minimum for a big)
    6'7" = 79   (H_67)
    6'8" = 80   (H_GUARD_MAX)

    "taller than 6'8""  -> height >  80
    "6'8"+"             -> height >= 80
    "under 6'5""        -> height <  77
    "6'5"+"             -> height >= 77

Percentiles are on a 0-1 scale, so "defensive-rebound percentile >= 60" is >= 0.60.

Missing values
    * A missing teammate share makes any condition that uses it FALSE (the rule is
      skipped) — except where the spec says "or the share is missing", which is
      written out explicitly.
    * A missing height also makes height conditions FALSE. (The spec only says what
      a missing height does in the guardrails; this is our choice for the rules.)

big() picks between the two big roles:
    blocks percentile >= defensive-rebound percentile -> UGA Big, otherwise Traditional Big
"""
import math

FLOOR_GENERAL = "Floor General"
COMBO_GUARD = "Combo Guard"
GUARD = "Guard"
SPECIALIST = "3pt Specialist"
THREE_AND_D = "3 and D Wing"
WING = "Wing"
TRAD_FORWARD = "Traditional Forward"
UGA_BIG = "UGA Big"
TRAD_BIG = "Traditional Big"

FAMILY = {
    FLOOR_GENERAL: "Guards", COMBO_GUARD: "Guards", GUARD: "Guards",
    SPECIALIST: "Wings", THREE_AND_D: "Wings", WING: "Wings",
    TRAD_FORWARD: "Bigs", UGA_BIG: "Bigs", TRAD_BIG: "Bigs",
}


# ---------------------------------------------------------------------------
# tiny helpers: every comparison is False when the value is missing
# ---------------------------------------------------------------------------

def missing(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def at_least(x, limit):
    return not missing(x) and x >= limit


def above(x, limit):
    return not missing(x) and x > limit


def below(x, limit):
    return not missing(x) and x < limit


# ---------------------------------------------------------------------------
# the rules
# ---------------------------------------------------------------------------

class Rules:
    """The seven proposal rules.

    `p` is one player as a dict with these keys:
        height_in, lead, lead2, inside, inside2, front,
        pctl_drb, pctl_blocks, pctl_steals,
        three_pa_share, usage, usage_median, raw_shooting
    """

    def __init__(self, c):
        self.H_WING = c["H_WING"]                     # 77 = 6'5"
        self.H_67 = c["H_67"]                         # 79 = 6'7"
        self.H_GUARD_MAX = c["H_GUARD_MAX"]           # 80 = 6'8"
        self.HALF = c["SHARE_THRESHOLD"]              # 0.50
        self.THREE_SHARE = c["THREE_SHARE_SPEC"]      # 0.60
        self.DRB_HIGH = c["DRB_PCTL_HIGH"]            # 0.60
        self.DRB_LOW = c["DRB_PCTL_LOW"]              # 0.50
        self.STEAL_MARGIN = c["STEAL_SHOOT_MARGIN"]   # 0.05

    def big(self, p):
        blocks = 0 if missing(p["pctl_blocks"]) else p["pctl_blocks"]
        drb = 0 if missing(p["pctl_drb"]) else p["pctl_drb"]
        return UGA_BIG if blocks >= drb else TRAD_BIG

    # ---- one method per group, in spec order --------------------------------

    def creation(self, p):
        h = p["height_in"]
        if above(h, self.H_GUARD_MAX):                          # taller than 6'8"
            return TRAD_FORWARD                                 # a creator at the big spot
        if at_least(p["lead"], self.HALF) or missing(p["lead"]):
            return FLOOR_GENERAL                                # best passer of the five
        if below(h, self.H_WING):                               # under 6'5"
            return COMBO_GUARD                                  # a better creator is on the floor
        if at_least(p["inside2"], self.HALF):
            return TRAD_FORWARD
        return WING

    def self_creation(self, p):
        h = p["height_in"]
        if below(h, self.H_WING):
            return COMBO_GUARD
        if at_least(h, self.H_GUARD_MAX) and at_least(p["inside2"], self.HALF):
            return TRAD_FORWARD
        return WING

    def shooting(self, p):
        h = p["height_in"]
        tall = at_least(h, self.H_67)                                   # 6'7"+
        plays_4_5 = at_least(p["front"], self.HALF)
        if tall and at_least(p["pctl_drb"], self.DRB_HIGH) and \
                (at_least(h, self.H_GUARD_MAX) or plays_4_5):
            return TRAD_FORWARD                                         # Stretch 4
        if tall and at_least(p["pctl_drb"], self.DRB_LOW) and plays_4_5:
            return TRAD_FORWARD                                         # borderline rebounder
        if at_least(p["three_pa_share"], self.THREE_SHARE):
            return SPECIALIST                                           # 60%+ shots are threes
        if at_least(h, self.H_WING) and below(p["usage"], p["usage_median"]):
            return THREE_AND_D
        if below(h, self.H_WING) and \
                at_least(p["pctl_steals"], p["raw_shooting"] - self.STEAL_MARGIN):
            return GUARD
        return SPECIALIST

    def steals(self, p):
        h = p["height_in"]
        if at_least(p["inside"], self.HALF):
            return self.big(p) if at_least(h, self.H_GUARD_MAX) else TRAD_FORWARD
        if at_least(p["inside2"], self.HALF) and at_least(h, self.H_WING):
            return TRAD_FORWARD
        if at_least(h, self.H_WING):
            return THREE_AND_D
        return GUARD

    def def_glass(self, p):
        if at_least(p["inside"], self.HALF):
            return self.big(p)
        return TRAD_FORWARD

    def blocks(self, p):
        h = p["height_in"]
        if at_least(p["inside"], self.HALF) or missing(p["inside"]):
            return UGA_BIG
        if at_least(p["inside2"], self.HALF):
            return TRAD_FORWARD                 # a shot-blocker beside a bigger interior player
        if at_least(h, self.H_WING):
            return THREE_AND_D
        return GUARD

    def inside(self, p):
        return self.big(p)

    # ---- all seven at once ---------------------------------------------------

    def propose_all(self, p):
        """{group: proposed role} for the seven groups."""
        return {
            "creation": self.creation(p),
            "self_creation": self.self_creation(p),
            "shooting": self.shooting(p),
            "steals": self.steals(p),
            "def_glass": self.def_glass(p),
            "blocks": self.blocks(p),
            "inside": self.inside(p),
        }
