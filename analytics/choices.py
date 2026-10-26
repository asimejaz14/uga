"""
analytics app ke choices (fixed values).

TextChoices ka faida (D-04): database mein sirf yahi values ja sakti hain,
"Floor general" jaisi typo nahi. Pehli value database mein jati hai,
doosri (label) admin / display ke liye hai.
"""
from django.db import models


class Role(models.TextChoices):
    """Spec ke 9 archetypes (Step 1 ka primary / secondary role)."""
    # Guards
    FLOOR_GENERAL = "floor_general", "Floor General"
    COMBO_GUARD = "combo_guard", "Combo Guard"
    GUARD = "guard", "Guard"
    # Wings
    THREE_PT_SPECIALIST = "three_pt_specialist", "3pt Specialist"
    THREE_AND_D_WING = "three_and_d_wing", "3 and D Wing"
    WING = "wing", "Wing"
    # Bigs
    TRADITIONAL_FORWARD = "traditional_forward", "Traditional Forward"
    UGA_BIG = "uga_big", "UGA Big"
    TRADITIONAL_BIG = "traditional_big", "Traditional Big"


class Family(models.TextChoices):
    """Primary role se nikalti hai. Level isi se replacement level chunta hai."""
    GUARDS = "guards", "Guards"
    WINGS = "wings", "Wings"
    BIGS = "bigs", "Bigs"


class Group(models.TextChoices):
    """Play types ke 7 gucchay. Har group ek role propose karta hai."""
    CREATION = "creation", "Creation"
    SELF_CREATION = "self_creation", "Self-creation"
    SHOOTING = "shooting", "Shooting"
    STEALS = "steals", "Steals"
    DEFENSIVE_GLASS = "defensive_glass", "Defensive glass"
    BLOCKS = "blocks", "Blocks"
    INSIDE = "inside", "Inside"


class Tier(models.TextChoices):
    """Level ka rang, WAR per 40 se (bars analytics/constants.py mein)."""
    DARK_GREEN = "dark_green", "Dark Green"
    LIGHT_GREEN = "light_green", "Light Green"
    YELLOW = "yellow", "Yellow"
    RED = "red", "Red"


class Confidence(models.TextChoices):
    NORMAL = "normal", "Normal"
    LOW = "low", "Low"  # pooled seasons ya fallback se placement


class RulesMode(models.TextChoices):
    """Season mein shot tags the (full) ya sirf purane proxies (coarse)."""
    FULL = "full", "Full (tagged play types)"
    COARSE = "coarse", "Coarse (proxies)"


class Sample(models.TextChoices):
    """Group score kis data par bana."""
    CURRENT = "current", "Current season (pooled rules ke saath)"
    THREE_SEASON = "three_season", "Three-season sample (sirf tiebreaker 4)"


class RunKind(models.TextChoices):
    ROLE = "role", "Role"
    LEVEL = "level", "Level"


class RunStatus(models.TextChoices):
    RUNNING = "running", "Running"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class DecidedBy(models.TextChoices):
    """Primary role ka faisla kis stage ne kiya (audit)."""
    CLEAR_TOP_GROUP = "clear_top_group", "Clear top group"
    TB_CREATOR = "tb_creator", "Tiebreaker 1: teammates (creator)"
    TB_INTERIOR = "tb_interior", "Tiebreaker 2: teammates (interior)"
    TB_LENGTH = "tb_length", "Tiebreaker 3: length"
    TB_LARGER_SAMPLE = "tb_larger_sample", "Tiebreaker 4: larger sample"
    TB_HIGHER_VOLUME = "tb_higher_volume", "Tiebreaker 5: higher volume"
    MATRIX_FIT_PLACEHOLDER = "matrix_fit_placeholder", "Fallback placeholder (A-02)"
    NO_DATA = "no_data", "No data, role nahi diya"


class PlayType(models.TextChoices):
    """
    Role ke play types (spec 2.4). Database mein sirf audit JSON (top4_play_types)
    mein naam ki shakal mein jate hain.
    """
    # --- Har season (base) ---
    ASSISTS = "assists", "Assists"
    AST_TO_THREE = "ast_to_three", "Assists to three"
    AST_TO_RIM = "ast_to_rim", "Assists to the rim"
    FT_TRIPS = "ft_trips", "FT trips"
    TRANSITION = "transition", "Transition"
    OWN_THREES = "own_threes", "Own threes"
    CS_THREES = "cs_threes", "Catch-and-shoot threes"
    CS_MID = "cs_mid", "Catch-and-shoot mid-range"
    STEALS = "steals", "Steals"
    BLOCKS = "blocks", "Blocks"
    DEF_REBOUNDS = "def_rebounds", "Defensive rebounds"
    OFF_REBOUNDS = "off_rebounds", "Offensive rebounds"
    PUTBACKS = "putbacks", "Putbacks"
    # --- Coarse proxies (tags ke baghair seasons) ---
    UNAST_RIM = "unast_rim", "Unassisted rim attempts"
    UNAST_MID = "unast_mid", "Unassisted mid-range 2s"
    AST_RIM_ATTEMPTS = "ast_rim_attempts", "Assisted rim attempts"
    # --- Tagged (shot tags wale seasons) ---
    DRIVING_LAYUPS = "driving_layups", "Driving layups"
    PULLUPS_2 = "pullups_2", "Pull-ups and step-backs"
    PULLUP_RANGE_2S = "pullup_range_2s", "Pull-up range 2s"
    FLOATERS = "floaters", "Floaters"
    PULLUPS_3 = "pullups_3", "Three-point pull-ups"
    CUT_ROLL = "cut_roll", "Cut and roll finishes"
    TIP_INS = "tip_ins", "Tip-ins"
    HOOKS = "hooks", "Hooks and turnarounds"
