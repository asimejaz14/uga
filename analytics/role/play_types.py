"""
Role steps R2 + R3: har player ke play-type COUNTS banana, phir unhein
RATES (per 100 possessions) mein badalna.

Spec ka asool: "counts enter; make-rates do not". Yahan sirf ginti hai,
koi FG% nahi. (Assisted share sirf ye batata hai ke shot pass se aaya ya
khud banaya; ye "kitna achha" nahi.)

Ye file PURE PYTHON hai (D-13).

Teen qisam ke play types (denominator alag alag):

    1. Base (pooled): R1 ke weights se seasons jama, phir pooled possessions par.
       Offense -> pooled off_poss; steals/blocks/def rebounds -> pooled def_poss.

    2. Tagged (sirf is season, kabhi pool nahi): sirf tagged games ke
       possessions (tagged_off_poss) par. Agar player ka koi tagged game nahi
       to value None (A-10), 0 nahi.

    3. Pull-up range 2s: sirf is season, lekin poore season ke off_poss par (A-11).

Misaal (spec 2.5): 140 assists / 1,400 possessions * 100 = 10.0 per 100.
"""
from analytics.choices import PlayType, RulesMode
from analytics.constants import (
    ASSIST_SHRINK_MAKES, CURRENT_SEASON_FULL_POSS_PLAY_TYPES,
    DEFENSIVE_PLAY_TYPES, RATE_PER, TAGGED_PLAY_TYPES,
)

# Ye columns seasons ke aar paar POOL hote hain (weights ke saath jama).
POOLED_FIELDS = (
    "assists", "ast_to_three", "ast_to_rim", "ft_trips", "transition_fga",
    "steals", "blocks", "drb", "orb", "putbacks",
    "fga_rim", "fgm_rim", "fgm_rim_ast",
    "fga_mid", "fgm_mid", "fgm_mid_ast",
    "fga_three", "fgm_three", "fgm_three_ast",
    "off_poss", "def_poss",
)

# Ye sirf IS season se aate hain (kabhi pool nahi).
CURRENT_ONLY_FIELDS = (
    "driving_layups", "pullups_2", "pullup_range_2s", "floaters", "pullups_3",
    "plain_rim_fga", "plain_rim_fgm", "plain_rim_fgm_ast",
    "tip_ins", "hooks_turnarounds", "tagged_off_poss", "off_poss",
)


# ---------------------------------------------------------------------------
# Chhote helpers
# ---------------------------------------------------------------------------

def pool_rows(rows_by_season, weights):
    """
    Kai seasons ki rows ko weights laga kar jama karo.

        rows_by_season = {2026: {"assists": 100, ...}, 2025: {"assists": 80, ...}}
        weights        = {2026: 1.0, 2025: 0.5}
        -> {"assists": 100 + 40 = 140, ...}

    Jis season ki row nahi (player nahi khela), us ka hissa 0.
    """
    pooled = {field: 0.0 for field in POOLED_FIELDS}
    for season, weight in weights.items():
        row = rows_by_season.get(season)
        if row is None:
            continue
        for field in POOLED_FIELDS:
            pooled[field] += (row.get(field) or 0) * weight
    return pooled


def shrunk_share(assisted_makes, makes, national_share):
    """
    Assisted share, national share ki taraf kheencha hua (spec 2.4):

        a = (assisted makes + 5 * national) / (makes + 5)

    Misaal: 2 makes, dono assisted, national 0.60 -> (2 + 3) / 7 = 0.714
    (raw 2/2 = 1.00 hota, jo 2 shots par zyada yaqeen hai).
    """
    return (assisted_makes + ASSIST_SHRINK_MAKES * national_share) / (makes + ASSIST_SHRINK_MAKES)


def per_100(count, possessions):
    """count / possessions * 100. Possessions 0 ya count None ho to None."""
    if count is None or not possessions:
        return None
    return count / possessions * RATE_PER


# ---------------------------------------------------------------------------
# R2: counts
# ---------------------------------------------------------------------------

def play_type_counts(pooled, current, national_share, rules_mode):
    """
    Ek player ke play-type counts.

    pooled:         pool_rows() ka natija (weights ke saath jama)
    current:        is season ki row (dict) ya None
    national_share: {"rim": .., "mid": .., "three": ..} is season ki (A-23)
    rules_mode:     RulesMode.FULL (tags) ya RulesMode.COARSE

    Wapas: {PlayType: count ya None}
    """
    # Assisted shares POOLED makes se (A-23: "rates are made from the pooled counts")
    a_rim = shrunk_share(pooled["fgm_rim_ast"], pooled["fgm_rim"], national_share["rim"])
    a_mid = shrunk_share(pooled["fgm_mid_ast"], pooled["fgm_mid"], national_share["mid"])
    a_three = shrunk_share(pooled["fgm_three_ast"], pooled["fgm_three"], national_share["three"])

    counts = {
        # Creation
        PlayType.ASSISTS: pooled["assists"],
        PlayType.AST_TO_THREE: pooled["ast_to_three"],
        PlayType.AST_TO_RIM: pooled["ast_to_rim"],
        # Self-creation (base)
        PlayType.FT_TRIPS: pooled["ft_trips"],
        PlayType.TRANSITION: pooled["transition_fga"],
        PlayType.OWN_THREES: pooled["fga_three"] * (1 - a_three),
        # Shooting
        PlayType.CS_THREES: pooled["fga_three"] * a_three,
        PlayType.CS_MID: pooled["fga_mid"] * a_mid,
        # Defense
        PlayType.STEALS: pooled["steals"],
        PlayType.BLOCKS: pooled["blocks"],
        PlayType.DEF_REBOUNDS: pooled["drb"],
        # Inside (base)
        PlayType.OFF_REBOUNDS: pooled["orb"],
        PlayType.PUTBACKS: pooled["putbacks"],
    }

    if rules_mode == RulesMode.COARSE:
        # Tags nahi: 3 proxies (spec 2.4 "coarse proxies")
        rim_not_putback = max(pooled["fga_rim"] - pooled["putbacks"], 0)
        counts[PlayType.UNAST_RIM] = rim_not_putback * (1 - a_rim)
        counts[PlayType.UNAST_MID] = pooled["fga_mid"] * (1 - a_mid)
        counts[PlayType.AST_RIM_ATTEMPTS] = rim_not_putback * a_rim
        return counts

    # Full mode: tagged play types, SIRF is season se
    has_tagged_games = bool(current and current.get("tagged_off_poss"))
    if has_tagged_games:
        a_plain_rim = shrunk_share(
            current.get("plain_rim_fgm_ast") or 0,
            current.get("plain_rim_fgm") or 0,
            national_share["rim"],  # A-09
        )
        counts[PlayType.DRIVING_LAYUPS] = current.get("driving_layups")
        counts[PlayType.PULLUPS_2] = current.get("pullups_2")
        counts[PlayType.FLOATERS] = current.get("floaters")
        counts[PlayType.PULLUPS_3] = current.get("pullups_3")
        counts[PlayType.TIP_INS] = current.get("tip_ins")
        counts[PlayType.HOOKS] = current.get("hooks_turnarounds")
        counts[PlayType.CUT_ROLL] = (current.get("plain_rim_fga") or 0) * a_plain_rim
    else:
        # A-10: koi tagged game nahi -> blank, skip (0 nahi)
        for play_type in TAGGED_PLAY_TYPES:
            counts[play_type] = None

    # Pull-up range 2s: tags ki zaroorat nahi, is season ka poora data (A-11)
    counts[PlayType.PULLUP_RANGE_2S] = current.get("pullup_range_2s") if current else None
    return counts


# ---------------------------------------------------------------------------
# R3: rates
# ---------------------------------------------------------------------------

def play_type_rates(counts, pooled, current):
    """
    Counts ko per-100 rates mein badlo, har play type apne denominator par.

    Wapas: {PlayType: rate ya None}
    """
    current_off = current.get("off_poss") if current else None
    current_tagged = current.get("tagged_off_poss") if current else None

    rates = {}
    for play_type, count in counts.items():
        if play_type in TAGGED_PLAY_TYPES:
            possessions = current_tagged
        elif play_type in CURRENT_SEASON_FULL_POSS_PLAY_TYPES:
            possessions = current_off
        elif play_type in DEFENSIVE_PLAY_TYPES:
            possessions = pooled["def_poss"]
        else:
            possessions = pooled["off_poss"]
        rates[play_type] = per_100(count, possessions)
    return rates


def player_rates(rows_by_season, weights, season, national_share, rules_mode):
    """
    R2 + R3 ek saath, ek player ke liye.

    rows_by_season: {season: row dict} (counts + possessions mila kar, loaders.py se)
    weights:        R1 ke PoolingResult.weights
    Wapas: {PlayType: rate ya None}
    """
    pooled = pool_rows(rows_by_season, weights)
    current = rows_by_season.get(season)
    counts = play_type_counts(pooled, current, national_share, rules_mode)
    return play_type_rates(counts, pooled, current)
