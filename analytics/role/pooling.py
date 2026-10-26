"""
Role step R1: har player ke liye tay karna ke us ka role KIS DATA se
parha jaye ga (pooling), aur us par kitna bharosa hai (confidence).

Spec ka asool: "placement reads possessions, not seasons". Yaani agar is
season player ne kam khela, to pichle season(s) ka data saath mila kar
300 possessions tak pohanchte hain.

Ye file PURE PYTHON hai: database nahi chhuti. Data loaders.py se aata hai.

Paanch halatein (status):

    ESTABLISHED   is season 300+ possessions
                  -> is season + pichla season aadha weight (0.5)
                  -> confidence normal

    POOLED        is season < 300, lekin is + pichla (poora weight) >= 300
                  -> confidence low

    POOLED_THREE  phir bhi < 300, lekin + us se pichla season >= 300
                  -> confidence low

    FALLBACK      teeno mila kar bhi < 300 (lekin kuch data hai)
                  -> confidence low, fallback = True (A-02 placeholder)

    NO_DATA       teeno seasons mein ek bhi possession nahi
                  -> role nahi diya jayega (A-02)

Spec ke 2026 numbers (V-03..V-05):
    normal 3,350 = ESTABLISHED
    pooled   319 = POOLED + POOLED_THREE
    fallback 1,309 = FALLBACK + NO_DATA
"""
from dataclasses import dataclass

from analytics.choices import Confidence
from analytics.constants import MIN_READ_POSS, ROLE_DEF_PREV_W, ROLE_LOW_MINUTE_PREV_W

ESTABLISHED = "established"
POOLED = "pooled"
POOLED_THREE = "pooled_three"
FALLBACK = "fallback"
NO_DATA = "no_data"


@dataclass(frozen=True)
class PoolingResult:
    """Ek player ka R1 faisla."""
    player_id: int
    status: str                # upar ki paanch halaton mein se ek
    weights: dict              # {season: weight}, jaise {2026: 1.0, 2025: 0.5}
    pooled_off_poss: float     # weights laga kar kul offensive possessions
    confidence: str            # Confidence.NORMAL ya Confidence.LOW
    fallback: bool             # True = read nahi hua (FALLBACK ya NO_DATA)
    history_complete: bool     # False = rule ko chahiye wala season data mein tha hi nahi

    @property
    def has_read(self):
        """Spec ka "read": pooling ke baad 300+ possessions."""
        return not self.fallback


def pooled_possessions(off_poss_by_season, weights):
    """
    Weights laga kar possessions ka jama.

        off_poss_by_season = {2026: 120, 2025: 400}
        weights            = {2026: 1.0, 2025: 1.0}
        -> 120*1.0 + 400*1.0 = 520

    Jis season ki row nahi (player us saal nahi khela) us ke 0 maane jate hain.
    """
    return sum(off_poss_by_season.get(season, 0) * weight for season, weight in weights.items())


def decide_pooling(player_id, season, off_poss_by_season, seasons_in_data):
    """
    Ek player ka R1 faisla.

    player_id:          Django Player id
    season:             jis season ka role nikalna hai, jaise 2026
    off_poss_by_season: is player ke offensive possessions, {season: off_poss}
                        (sirf woh seasons jin ki row mojood hai)
    seasons_in_data:    database mein kaunse seasons hain, jaise {2024, 2025, 2026}
                        (history_complete ke liye)
    """
    this_season = off_poss_by_season.get(season, 0)
    prev = season - 1
    prev2 = season - 2

    if this_season >= MIN_READ_POSS:
        # Established: is season kaafi khela. Pichla season sirf aadha.
        weights = {season: 1.0, prev: ROLE_DEF_PREV_W}
        status = ESTABLISHED
    else:
        # Low-minute: pichla season poore weight par.
        weights = {season: 1.0, prev: ROLE_LOW_MINUTE_PREV_W}
        if pooled_possessions(off_poss_by_season, weights) >= MIN_READ_POSS:
            status = POOLED
        else:
            # Ab bhi kam: us se pichla season bhi.
            weights[prev2] = ROLE_LOW_MINUTE_PREV_W
            total = pooled_possessions(off_poss_by_season, weights)
            if total >= MIN_READ_POSS:
                status = POOLED_THREE
            elif total > 0:
                status = FALLBACK
            else:
                status = NO_DATA

    # Jo purane seasons is rule ne maange, kya woh database mein the?
    # (Player ka us saal na khelna theek hai; season ka data hi na hona adhoori history hai.)
    needed_past_seasons = [s for s in weights if s != season]
    history_complete = all(s in seasons_in_data for s in needed_past_seasons)

    return PoolingResult(
        player_id=player_id,
        status=status,
        weights=weights,
        pooled_off_poss=pooled_possessions(off_poss_by_season, weights),
        confidence=Confidence.NORMAL if status == ESTABLISHED else Confidence.LOW,
        fallback=status in (FALLBACK, NO_DATA),
        history_complete=history_complete,
    )


def decide_pooling_for_season(season, frame_player_ids, off_poss_lookup, seasons_in_data):
    """
    Poore frame ke liye R1.

    frame_player_ids: jin players ko place karna hai (A-17: D1 team + counts row)
    off_poss_lookup:  {(player_id, season): off_poss} — loaders.py se
    Wapas: {player_id: PoolingResult}
    """
    results = {}
    for player_id in frame_player_ids:
        off_poss_by_season = {
            s: off_poss_lookup[(player_id, s)]
            for s in (season, season - 1, season - 2)
            if (player_id, s) in off_poss_lookup
        }
        results[player_id] = decide_pooling(player_id, season, off_poss_by_season, seasons_in_data)
    return results
