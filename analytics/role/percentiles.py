"""
Role steps R4 + R5: rates ko PERCENTILES mein badalna, phir play types ko
7 GROUPS mein jama kar ke group score banana.

Ye file PURE PYTHON hai (D-13).

R4 — play-type percentile (spec 2.5):
    "share of qualified players this season with a lower rate" (0 se 1)
    Population hamesha QUALIFIED players hain, chahe player khud qualified na ho
    (A-18). "Lower" strictly lower hai: barabar wale nahi gine jate.

    Misaal: 4 qualified players ke assists rates [2, 4, 6, 8].
            rate 6 -> neeche 2 players (2, 4) -> 2/4 = 0.50
            rate 7 -> neeche 3 players            -> 0.75

R5 — group score (spec 2.7 Stage B):
    raw score   = group ke andar us ke DO SAB SE OONCHE percentiles ka mean
                  (sirf ek mojood ho to wahi; koi nahi to None)
    group score = raw score ka percentile, usi GROUP ke qualified raw scores mein

    Misaal (spec): Creation percentiles 0.85, 0.78, 0.60
                   -> raw (0.85 + 0.78) / 2 = 0.815
                   -> qualified players ke Creation raw scores mein percentile -> 0.88
"""
from bisect import bisect_left


# ---------------------------------------------------------------------------
# Percentile ka buniyadi function
# ---------------------------------------------------------------------------

def percentile_of(value, sorted_population):
    """
    sorted_population mein kitne hisse ki value `value` se STRICTLY kam hai (0-1).

    bisect_left sorted list mein woh jagah deta hai jahan `value` daali jaye
    to woh barabar walon se PEHLE aaye; yaani us se pehle jitni values hain,
    sab strictly kam hain.
    """
    if value is None or not sorted_population:
        return None
    return bisect_left(sorted_population, value) / len(sorted_population)


def sorted_population(values_by_player, qualified_ids):
    """Qualified players ki (None ke baghair) values, chhoti se bari."""
    return sorted(
        values_by_player[p] for p in qualified_ids
        if p in values_by_player and values_by_player[p] is not None
    )


# ---------------------------------------------------------------------------
# R4: play-type percentiles
# ---------------------------------------------------------------------------

def play_type_percentiles(rates, qualified_ids, play_types):
    """
    rates:         {player_id: {PlayType: rate ya None}}  (R3 se)
    qualified_ids: qualified players ke ids
    play_types:    jin play types ke percentiles chahiyein (is season ke mode ke)

    Wapas: {player_id: {PlayType: percentile ya None}}
    """
    result = {player_id: {} for player_id in rates}
    for play_type in play_types:
        values = {p: r.get(play_type) for p, r in rates.items()}
        population = sorted_population(values, qualified_ids)
        for player_id, value in values.items():
            result[player_id][play_type] = percentile_of(value, population)
    return result


# ---------------------------------------------------------------------------
# R5: group scores
# ---------------------------------------------------------------------------

def group_raw_score(percentiles, members):
    """
    Group ke members mein se do sab se oonche percentiles ka mean.

    percentiles: {PlayType: percentile ya None} (ek player ke)
    members:     is group ke play types
    """
    present = sorted(
        (percentiles.get(pt) for pt in members if percentiles.get(pt) is not None),
        reverse=True,
    )
    if not present:
        return None
    top_two = present[:2]
    return sum(top_two) / len(top_two)


def group_scores(percentiles, qualified_ids, groups):
    """
    percentiles:   {player_id: {PlayType: percentile}}  (R4 se)
    groups:        {Group: [PlayType, ...]}  (constants.GROUP_PLAY_TYPES[mode])

    Wapas: {player_id: {Group: (raw_score, group_score)}}
    """
    result = {player_id: {} for player_id in percentiles}
    for group, members in groups.items():
        raw = {p: group_raw_score(pcts, members) for p, pcts in percentiles.items()}
        population = sorted_population(raw, qualified_ids)
        for player_id, raw_score in raw.items():
            result[player_id][group] = (raw_score, percentile_of(raw_score, population))
    return result


def top_play_types(percentiles, n=4):
    """
    Audit ke liye: n sab se oonche play-type percentiles,
    [{"play_type": "assists", "pct": 0.85}, ...]  (RolePlacement.top4_play_types)
    """
    ranked = sorted(
        ((pt, pct) for pt, pct in percentiles.items() if pct is not None),
        key=lambda item: item[1],
        reverse=True,
    )
    return [{"play_type": str(pt), "pct": round(pct, 4)} for pt, pct in ranked[:n]]
