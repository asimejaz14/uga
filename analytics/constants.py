"""
Spec ke constants (D-05). Spec badle to yahi file badlegi, aur git history
batayegi kab aur kyun.

Har constant ke saath spec ka hawala hai. Jo value spec ki nahi balki hamari
assumption hai, us par ASSUMPTIONS.md ka ID likha hai.

Abhi: shared + Level ke constants. Role ke rule thresholds Phase 4b mein.
"""
from .choices import Family, Group, PlayType, Role, RulesMode, Tier

SPEC_VERSION = "v9.1"


# ---------------------------------------------------------------------------
# Role -> Family
# ---------------------------------------------------------------------------

# Spec: "Family comes from the role the rules pick, not from deployment."
ROLE_FAMILY = {
    Role.FLOOR_GENERAL: Family.GUARDS,
    Role.COMBO_GUARD: Family.GUARDS,
    Role.GUARD: Family.GUARDS,
    Role.THREE_PT_SPECIALIST: Family.WINGS,
    Role.THREE_AND_D_WING: Family.WINGS,
    Role.WING: Family.WINGS,
    Role.TRADITIONAL_FORWARD: Family.BIGS,
    Role.UGA_BIG: Family.BIGS,
    Role.TRADITIONAL_BIG: Family.BIGS,
}


def family_for_role(role):
    """
    Role se family. Role None ho (no data, A-02) to None wapas aata hai,
    jis ka matlab Level mein overall replacement lagega.
    """
    if role is None:
        return None
    return ROLE_FAMILY[Role(role)]


# ---------------------------------------------------------------------------
# Shared: shots aur assisted share
# ---------------------------------------------------------------------------

# Har zone ke make ke points.
SHOT_POINTS = {"rim": 2, "mid": 2, "three": 3}

# Assisted share ko national share ki taraf kitne "nakli makes" se kheencha jaye.
# a = (assisted makes + 5 * national) / (makes + 5)       (spec 2.4, 3.5)
ASSIST_SHRINK_MAKES = 5


# ---------------------------------------------------------------------------
# Level: event prices (spec 3.4)
# ---------------------------------------------------------------------------

# Ek average possession ki qeemat. Har season fixed, jaan boojh kar.
PPP = 1.075

# Miss ke baad offense kitni dafa ball wapas le leti hai.
OREB_RECOVERY_RATE = 0.28

# Kisi bhi miss ki qeemat shooter ke liye: 0.28 * 1.075 - 1.075 = -0.774
MISS_VALUE = OREB_RECOVERY_RATE * PPP - PPP

# Free throws. Made +0.530, missed -0.470 (dono ka base 0.47).
FT_BASELINE = 0.47
FT_MADE_VALUE = 1 - FT_BASELINE      # +0.530
FT_MISSED_VALUE = -FT_BASELINE       # -0.470

# A-04: engine value 0.785 (derived value 0.774 hoti). Q-16 / readback Q10.
OFF_REBOUND_VALUE = 0.785
DEF_REBOUND_VALUE = 0.0              # miss shooter ko pehle hi charge ho chuka
STEAL_VALUE = PPP                    # +1.075
TURNOVER_VALUE = -PPP                # -1.075
BLOCK_VALUE = 0.750                  # derivation spec mein "open", value fixed
TECHNICAL_FREE_THROWS = 2            # technical = -2 * league FT%


# ---------------------------------------------------------------------------
# Level: replacement, points per win, WAR, tier (spec 3.6 - 3.9)
# ---------------------------------------------------------------------------

COVERAGE_MIN = 0.80                  # is se kam = not rated

BENCH_MIN_MINUTES = 50               # replacement band: 50-149 minutes, D1 team
BENCH_MAX_MINUTES = 149

# Family gap season +-1 par pool hota hai, spec ke data ke kinaron par clip
# (2015 aur 2026). Pehle season ke liye "s-1" ka na hona adhoori history nahi.
LEVEL_FIRST_SEASON = 2015

PPW_GAMES_SCALE = 31                 # x = margin/game * 31, y = wins/game * 31
PPW_MIN_GAMES = 10                   # sirf 10+ games wali D1 teams

RELIABILITY_MINUTES = 400            # WAR = ... * min(1, minutes / 400)
LEVEL_QUALIFIED_MINUTES = 400        # tier population: 400+ min, rated, D1

# A-15: 2015-2026 pooled percentiles, spec se constant. Oonche se neeche.
TIER_BARS = (
    (0.1489, Tier.DARK_GREEN),
    (0.0913, Tier.LIGHT_GREEN),
    (0.0340, Tier.YELLOW),
)
TIER_BELOW_BARS = Tier.RED


# ---------------------------------------------------------------------------
# Role: pooling (spec 2.3)
# ---------------------------------------------------------------------------

# "Read" hone ke liye kam az kam itne offensive possessions (pooling ke baad).
MIN_READ_POSS = 300

# Established player (is season 300+): pichla season aadhe weight par.
ROLE_DEF_PREV_W = 0.5

# Low-minute player: pichla (aur zaroorat ho to us se pichla) season poore weight par.
ROLE_LOW_MINUTE_PREV_W = 1.0


# ---------------------------------------------------------------------------
# Role: play types aur groups (spec 2.4, 2.5, 2.7 Stage A)
# ---------------------------------------------------------------------------

# Assisted share ka shrink, aur rates "per 100 possessions".
RATE_PER = 100

# Ye play types DEFENSIVE possessions par bante hain; baaqi sab offensive.
DEFENSIVE_PLAY_TYPES = {PlayType.STEALS, PlayType.BLOCKS, PlayType.DEF_REBOUNDS}

# Shot-tag wale play types: sirf is season, sirf tagged games ke possessions par,
# kabhi pool nahi (spec: "2026 shot tags: 2026 only, never pooled").
TAGGED_PLAY_TYPES = {
    PlayType.DRIVING_LAYUPS, PlayType.PULLUPS_2, PlayType.FLOATERS,
    PlayType.PULLUPS_3, PlayType.CUT_ROLL, PlayType.TIP_INS, PlayType.HOOKS,
}

# Pull-up range 2s: sirf is season, lekin POORE season ke off possessions par (A-11).
CURRENT_SEASON_FULL_POSS_PLAY_TYPES = {PlayType.PULLUP_RANGE_2S}

# 7 groups ke members. Full = shot tags wala season (2026), coarse = baaqi.
GROUP_PLAY_TYPES = {
    RulesMode.FULL: {
        Group.CREATION: [PlayType.ASSISTS, PlayType.AST_TO_THREE, PlayType.AST_TO_RIM],
        Group.SELF_CREATION: [
            PlayType.DRIVING_LAYUPS, PlayType.PULLUPS_2, PlayType.PULLUP_RANGE_2S,
            PlayType.FLOATERS, PlayType.FT_TRIPS, PlayType.TRANSITION,
            PlayType.OWN_THREES, PlayType.PULLUPS_3,
        ],
        Group.SHOOTING: [PlayType.CS_THREES, PlayType.CS_MID],
        Group.STEALS: [PlayType.STEALS],
        Group.DEFENSIVE_GLASS: [PlayType.DEF_REBOUNDS],
        Group.BLOCKS: [PlayType.BLOCKS],
        Group.INSIDE: [
            PlayType.OFF_REBOUNDS, PlayType.PUTBACKS, PlayType.TIP_INS,
            PlayType.CUT_ROLL, PlayType.HOOKS,
        ],
    },
    RulesMode.COARSE: {
        Group.CREATION: [PlayType.ASSISTS, PlayType.AST_TO_THREE, PlayType.AST_TO_RIM],
        Group.SELF_CREATION: [
            PlayType.UNAST_RIM, PlayType.UNAST_MID, PlayType.FT_TRIPS,
            PlayType.TRANSITION, PlayType.OWN_THREES,
        ],
        Group.SHOOTING: [PlayType.CS_THREES, PlayType.CS_MID],
        Group.STEALS: [PlayType.STEALS],
        Group.DEFENSIVE_GLASS: [PlayType.DEF_REBOUNDS],
        Group.BLOCKS: [PlayType.BLOCKS],
        Group.INSIDE: [PlayType.OFF_REBOUNDS, PlayType.PUTBACKS, PlayType.AST_RIM_ATTEMPTS],
    },
}

# Qualified (percentiles ki population): Torvik minutes% >= 40 aur is season 300+.
QUALIFIED_MIN_PCT = 40


# ---------------------------------------------------------------------------
# Role: teammate shares (spec 2.6)
# ---------------------------------------------------------------------------

# Possession tab ginta hai jab us ki side ke 5 mein se kam az kam itno ka "read" ho.
MIN_READ_TEAMMATES = 4

# Har share ke liye kam az kam itni aisi possessions; warna share NULL (rule skip).
MIN_SHARE_POSS = 200


# ---------------------------------------------------------------------------
# Role: group rules, guardrails, tiebreakers (spec 2.7 Stage C-F)
# ---------------------------------------------------------------------------

# Heights inches mein (Q-15). Rules ke alfaaz ka matlab:
#   "under 6'5\""   -> height <  H_6_5
#   "6'5\"+"        -> height >= H_6_5
#   "6'7\"+"        -> height >= H_6_7
#   "6'8\"+"        -> height >= H_6_8
#   "taller than 6'8\"" -> height > H_6_8
H_6_5 = 77     # wing length = big minimum
H_6_7 = 79
H_6_8 = 80     # guard maximum

# "X of the five on 50%+"
SHARE_MAJORITY = 0.50

# Shooting group rule ke thresholds (percentiles 0-1 scale par, A-12)
SHOOTING_DREB_PCT_HIGH = 0.60
SHOOTING_DREB_PCT_LOW = 0.50
THREE_SPECIALIST_SHARE = 0.60   # "60%+ of his shots are threes" (A-13)
GUARD_STEALS_MARGIN = 0.05      # steals pct >= shooting raw - 0.05

# Close call: top proposal se itne andar alag role wali proposal
DEF_CLOSE = 0.10

# Big roles (guardrail: 6'5"+ chahiye) aur guard roles (6'8" ya kam)
BIG_ROLES = {Role.UGA_BIG, Role.TRADITIONAL_BIG}
GUARD_ROLES = {Role.FLOOR_GENERAL, Role.COMBO_GUARD, Role.GUARD}
WING_ROLES = {Role.THREE_PT_SPECIALIST, Role.THREE_AND_D_WING, Role.WING}


def constants_snapshot():
    """
    Is module ke saare UPPER_CASE constants ek dict mein (JSON ke qabil).
    CalculationRun.constants_snapshot mein save hota hai (D-06).
    """
    snapshot = {}
    for name, value in globals().items():
        if not name.isupper():
            continue
        if name == "ROLE_FAMILY":
            value = {str(k): str(v) for k, v in value.items()}
        elif name == "TIER_BARS":
            value = [[bar, str(tier)] for bar, tier in value]
        elif name == "GROUP_PLAY_TYPES":
            value = {str(m): {str(g): [str(p) for p in pts] for g, pts in groups.items()}
                     for m, groups in value.items()}
        elif isinstance(value, set):
            value = sorted(str(v) for v in value)
        elif isinstance(value, str) and hasattr(value, "label"):
            value = str(value)
        snapshot[name] = value
    return snapshot
