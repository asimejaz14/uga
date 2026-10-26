"""
Role ke steps ko JORNE wala module: loaders se data, pure functions se hisaab.

Har check command (aur baad mein compute_role) yahi functions bulati hai,
taake R1-R5 ka code har command mein dobara na likhna pare.

Ye file database PARHTI hai (loaders ke zariye) lekin kuch LIKHTI nahi.
"""
from dataclasses import dataclass, field

from analytics import loaders
from analytics.constants import GROUP_PLAY_TYPES
from analytics.role import pooling
import dataclasses
import statistics

from analytics.choices import DecidedBy, Group, PlayType
from analytics.constants import MIN_READ_POSS
from analytics.role.percentiles import group_scores, play_type_percentiles
from analytics.role.placement import decide_role
from analytics.role.rules import PlayerFacts
from analytics.role.shares import compute_shares
from analytics.role.play_types import player_rates


@dataclass
class RoleSeason:
    """Ek season ke Role ka adhoora (R1-R5 tak) hisaab."""
    season: int
    rules_mode: str
    frame: list                      # player ids (A-17)
    qualified: set                   # percentiles ki population
    rows: dict                       # {(player_id, season): row}  loaders.role_rows_lookup
    pooling: dict                    # {player_id: PoolingResult}            R1
    rates: dict = field(default_factory=dict)        # {player_id: {PlayType: rate}}        R2+R3
    percentiles: dict = field(default_factory=dict)  # {player_id: {PlayType: pct}}         R4
    groups: dict = field(default_factory=dict)       # {player_id: {Group: (raw, score)}}   R5
    heights: dict = field(default_factory=dict)      # {player_id: inches}
    shares: dict = field(default_factory=dict)       # {player_id: Shares}                  R6
    share_totals: dict = field(default_factory=dict) # R6 validation ginti
    torvik: dict = field(default_factory=dict)       # {player_id: (usage, three_pa_share)}
    usage_median: float = None
    three_season: dict = field(default_factory=dict) # {player_id: {Group: score}}   R9 (tiebreaker 4)
    three_season_groups: dict = field(default_factory=dict)  # {player_id: {Group: (raw, score)}} (save ke liye)
    decisions: dict = field(default_factory=dict)    # {player_id: Decision ya None} R7+R8

    @property
    def group_definitions(self):
        return GROUP_PLAY_TYPES[self.rules_mode]


def build_role_season(season, with_shares=False):
    """
    R1 se R5 tak, ek season ke liye. with_shares=True ho to R6 bhi
    (possessions parhne ki wajah se thora waqt leta hai).
    """
    seasons = [season, season - 1, season - 2]
    frame = loaders.role_frame(season)
    rows = loaders.role_rows_lookup(frame, seasons)

    # R1
    off_lookup = {key: row["off_poss"] for key, row in rows.items()}
    pool_results = pooling.decide_pooling_for_season(season, frame, off_lookup, loaders.seasons_in_data())

    data = RoleSeason(
        season=season,
        rules_mode=loaders.rules_mode_for_season(season),
        frame=frame,
        qualified=loaders.qualified_player_ids(season, frame),
        rows=rows,
        pooling=pool_results,
    )

    # R2 + R3 (NO_DATA players ke rates nahi bante)
    national_share = loaders.national_assist_shares(season)
    for player_id, result in pool_results.items():
        if result.status == pooling.NO_DATA:
            continue
        rows_by_season = {s: rows[(player_id, s)] for s in seasons if (player_id, s) in rows}
        data.rates[player_id] = player_rates(
            rows_by_season, result.weights, season, national_share, data.rules_mode
        )

    # R4
    all_play_types = [pt for members in data.group_definitions.values() for pt in members]
    data.percentiles = play_type_percentiles(data.rates, data.qualified, all_play_types)

    # R5
    data.groups = group_scores(data.percentiles, data.qualified, data.group_definitions)

    data.heights = loaders.heights(season, frame)
    if with_shares:
        add_shares(data)
    return data


def add_shares(data):
    """R6: teammate shares. Rates R3 (pooled) se, read R1 se."""
    assist_rate = {}
    interior_rate = {}
    for player_id, rates in data.rates.items():
        assist_rate[player_id] = rates.get(PlayType.ASSISTS) or 0.0
        # A-20: teeno alag rates ka jama (blocks defensive possessions par)
        interior_rate[player_id] = (
            (rates.get(PlayType.OFF_REBOUNDS) or 0.0)
            + (rates.get(PlayType.BLOCKS) or 0.0)
            + (rates.get(PlayType.PUTBACKS) or 0.0)
        )
    has_read = {p for p, r in data.pooling.items() if r.has_read}

    data.shares, data.share_totals = compute_shares(
        loaders.offensive_lineup_counts(data.season),
        assist_rate, interior_rate, has_read, data.heights,
    )



# ---------------------------------------------------------------------------
# R9: three-season sample (sirf tiebreaker 4)
# ---------------------------------------------------------------------------

THREE_SEASON_WEIGHT = 1.0   # spec: "full weight by possessions"


def add_three_season(data):
    """
    Har player ka 3-season pooled sample (s, s-1, s-2 poore weight), sirf agar
    pooled 300+ possessions hon ("a three-season read exists").
    Percentiles aur group scores usi tarah, qualified players ki population (Q-11).
    """
    season = data.season
    weights = {season: THREE_SEASON_WEIGHT, season - 1: THREE_SEASON_WEIGHT, season - 2: THREE_SEASON_WEIGHT}
    national_share = loaders.national_assist_shares(season)

    rates = {}
    for player_id in data.frame:
        rows_by_season = {s: data.rows[(player_id, s)] for s in weights if (player_id, s) in data.rows}
        pooled_poss = sum(row["off_poss"] for row in rows_by_season.values())
        if pooled_poss < MIN_READ_POSS:
            continue
        rates[player_id] = player_rates(rows_by_season, weights, season, national_share, data.rules_mode)

    all_play_types = [pt for members in data.group_definitions.values() for pt in members]
    percentiles = play_type_percentiles(rates, data.qualified, all_play_types)
    scores = group_scores(percentiles, data.qualified, data.group_definitions)
    data.three_season_groups = scores
    data.three_season = {p: {g: s for g, (_, s) in groups.items()} for p, groups in scores.items()}


# ---------------------------------------------------------------------------
# R7 + R8: rules aur faisla
# ---------------------------------------------------------------------------

def player_facts(data, player_id):
    """Rules ke liye ek player ki PlayerFacts."""
    shares = data.shares.get(player_id)
    usage, three_pa_share = data.torvik.get(player_id, (None, None))
    shooting = data.groups.get(player_id, {}).get(Group.SHOOTING, (None, None))
    return PlayerFacts(
        height=data.heights.get(player_id),
        lead=shares.lead if shares else None,
        inside=shares.inside if shares else None,
        inside2=shares.inside2 if shares else None,
        front=shares.front if shares else None,
        percentiles=data.percentiles.get(player_id, {}),
        shooting_raw=shooting[0],
        usage=usage,
        usage_median=data.usage_median,
        three_pa_share=three_pa_share,
    )


def add_decisions(data):
    """Har frame player ka Role faisla (R7 + R8)."""
    data.torvik = loaders.torvik_role_values(data.season, data.frame)
    qualified_usage = [data.torvik[p][0] for p in data.qualified if p in data.torvik]
    data.usage_median = statistics.median(qualified_usage) if qualified_usage else None

    for player_id in data.frame:
        result = data.pooling[player_id]
        if result.status == pooling.NO_DATA or player_id not in data.groups:
            data.decisions[player_id] = None
            continue
        decision = decide_role(
            data.groups[player_id],
            player_facts(data, player_id),
            data.three_season.get(player_id),
        )
        if decision is not None and result.fallback:
            # A-02: matrix fit nahi; wahi rules, lekin faisla placeholder ke naam
            decision = dataclasses.replace(decision, decided_by=DecidedBy.MATRIX_FIT_PLACEHOLDER)
        data.decisions[player_id] = decision


def build_full_role_season(season):
    """R1 se R9 tak, poora Role (save ke baghair)."""
    data = build_role_season(season, with_shares=True)
    add_three_season(data)
    add_decisions(data)
    return data
