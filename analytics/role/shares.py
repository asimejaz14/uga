"""
Role step R6: teammate shares — "kis ke SAATH khelta hai" (spec 2.6).

Har offensive possession mein court par 5 players hote hain. Un 5 ko do
tarah rank karte hain, har player ke SEASON (pooled) rate par:

    ranking 1: assists per 100                                -> lead, lead2
    ranking 2: (off rebounds + blocks + putbacks) per 100     -> inside, inside2

Aur height par:                                               -> front

    lead    = kitne % possessions mein woh 5 mein sab se bara passer tha (rank 1)
    lead2   = kitne % mein top 2 mein tha               (hamesha >= lead)
    inside  = kitne % mein sab se bara interior player tha
    inside2 = kitne % mein top 2 interior mein tha
    front   = kitne % mein 5 mein se do sab se lambon mein tha (slot 4-5)

Muqabla TEAMMATES se hai, league se nahi: kamzor team ka average passer bhi
ooncha `lead` le sakta hai. Sawal hai "is team ka offense kaun chalata hai".

Sharten (spec + ASSUMPTIONS):
    - Possession tab ginta hai jab us side ke 5 mein se 4+ ka "read" ho.
    - Ranking sirf read wale players mein (A-21). Jis player ka khud read
      nahi, us ke shares nahi bante.
    - Barabar rate: dono ko ek hi rank (A-19). rank = 1 + jitno ka rate zyada hai.
    - Interior rate = ORB/100 + BLK/100 + putbacks/100 (A-20).
    - Height missing ho to us possession ki front ranking sirf height walon
      mein; player ki apni height missing to front NULL (A-22).
    - Har share ke liye 200+ aisi possessions, warna NULL (rule skip hota hai).

Raftaar: ek hi 5 players ka lineup season mein sau dafa aata hai. Is liye
loader har lineup ko ek dafa ginti ke saath deta hai, aur ranking har
lineup ki sirf ek dafa hoti hai.

Ye file PURE PYTHON hai (D-13).
"""
from dataclasses import dataclass

from analytics.constants import MIN_READ_TEAMMATES, MIN_SHARE_POSS


@dataclass(frozen=True)
class Shares:
    """Ek player ke teammate shares (0-1 ya None)."""
    valid_poss: int
    lead: float = None
    lead2: float = None
    inside: float = None
    inside2: float = None
    front: float = None


def rank_within(players, value_of):
    """
    Har player ka rank, value ke hisaab se (bari value = rank 1).
    Barabar values ko ek hi rank (A-19).

        values {A: 5, B: 9, C: 5}  ->  {B: 1, A: 2, C: 2}
    """
    return {
        p: 1 + sum(1 for q in players if value_of[q] > value_of[p])
        for p in players
    }


def compute_shares(lineup_counts, assist_rate, interior_rate, has_read, heights):
    """
    lineup_counts: {(p1, p2, p3, p4, p5): kitni possessions}   (loaders se)
    assist_rate:   {player_id: assists per 100}                 (R3, pooled)
    interior_rate: {player_id: ORB + BLK + putbacks per 100}    (R3, pooled)
    has_read:      set of player ids jin ka read hai            (R1)
    heights:       {player_id: inches}                          (Torvik)

    Wapas: (shares, totals)
        shares: {player_id: Shares}  — sirf read wale players
        totals: validation ke liye ginti (command print karti hai)
    """
    valid = {}       # player -> kitni valid possessions
    tallies = {}     # player -> [lead, lead2, inside, inside2, front, front_poss]
    totals = {"possessions": 0, "valid_possessions": 0, "lead_firsts": 0}

    for lineup, n in lineup_counts.items():
        totals["possessions"] += n

        readers = [p for p in lineup if p in has_read]
        if len(readers) < MIN_READ_TEAMMATES:
            continue  # spec: 4+ of the five must have a read
        totals["valid_possessions"] += n

        lead_rank = rank_within(readers, assist_rate)
        inside_rank = rank_within(readers, interior_rate)

        with_height = [p for p in lineup if p in heights]
        height_rank = rank_within(with_height, heights)

        for p in readers:
            valid[p] = valid.get(p, 0) + n
            t = tallies.setdefault(p, [0, 0, 0, 0, 0, 0])
            if lead_rank[p] == 1:
                t[0] += n
                totals["lead_firsts"] += n
            if lead_rank[p] <= 2:
                t[1] += n
            if inside_rank[p] == 1:
                t[2] += n
            if inside_rank[p] <= 2:
                t[3] += n
            if p in heights:
                t[5] += n                 # front ka denominator: jab us ki height pata ho
                if height_rank[p] <= 2:   # do sab se lambon mein (slot 4-5)
                    t[4] += n

    shares = {}
    for p, n_valid in valid.items():
        t = tallies[p]
        if n_valid < MIN_SHARE_POSS:
            shares[p] = Shares(valid_poss=n_valid)  # sab shares NULL
            continue
        shares[p] = Shares(
            valid_poss=n_valid,
            lead=t[0] / n_valid,
            lead2=t[1] / n_valid,
            inside=t[2] / n_valid,
            inside2=t[3] / n_valid,
            front=(t[4] / t[5]) if t[5] >= MIN_SHARE_POSS else None,
        )
    return shares, totals
