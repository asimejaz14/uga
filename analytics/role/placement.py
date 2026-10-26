"""
Role step R8: proposals se aakhri faisla (spec 2.7 Stage D-F, 2.8).

    Stage D  guardrails:   na-mumkin proposals hatao
                           (big role 6'5" se chhota, guard role 6'8" se lamba)
    Stage E  ranking:      group score ke hisaab se, high -> low
             close call:   top ke 0.10 ke andar ALAG role wali proposals
    Stage F  tiebreakers:  close call ho to, order mein
    Output:  primary, secondary, family, winning group, decided_by

Tiebreaker ka asool (spec): har tiebreaker tab hi lagta hai jab woh kam az
kam ek candidate HATAYE aur kam az kam ek BACHAYE. Jo tiebreaker sirf ek
candidate chhore, faisla usi ka.

Ye file PURE PYTHON hai (D-13).
"""
from dataclasses import dataclass

from analytics.choices import DecidedBy, Family, Role
from analytics.constants import (
    BIG_ROLES, DEF_CLOSE, GUARD_ROLES, H_6_5, H_6_8, WING_ROLES, family_for_role,
)
from analytics.role.rules import majority, propose_role


@dataclass
class Proposal:
    """Ek group ki proposal (GroupScore row ban'ti hai)."""
    group: str
    raw_score: float
    score: float
    role: str
    dropped_by_guardrail: bool = False


@dataclass(frozen=True)
class Decision:
    """Ek player ka aakhri Role faisla."""
    primary: str
    secondary: str
    family: str
    winning_group: str
    decided_by: str
    proposals: list          # saari Proposal objects (audit)


# ---------------------------------------------------------------------------
# Stage C + D: proposals aur guardrails
# ---------------------------------------------------------------------------

def make_proposals(group_scores, facts):
    """
    group_scores: {Group: (raw, score)}  (R5)
    Har us group ki proposal jis ka score mojood ho.
    """
    proposals = []
    for group, (raw, score) in group_scores.items():
        if score is None:
            continue
        proposals.append(Proposal(group=group, raw_score=raw, score=score, role=propose_role(group, facts)))
    return proposals


def breaks_guardrail(role, height):
    """
    Spec Stage D: big role ko 6'5"+ chahiye, guard role ko 6'8" ya kam.
    Height pata nahi to dono pass.
    """
    if height is None:
        return False
    if role in BIG_ROLES and height < H_6_5:
        return True
    if role in GUARD_ROLES and height > H_6_8:
        return True
    return False


# ---------------------------------------------------------------------------
# Stage F: tiebreakers. Har function candidates leta hai aur "rakhne wale"
# candidates wapas karta hai, ya None agar tiebreaker lagu hi nahi hota.
# ---------------------------------------------------------------------------

def tb_creator(candidates, facts, three_season):
    """1. Teammates (creator): lead mojood ho aur Floor General candidate ho."""
    if facts.lead is None or not any(c.role == Role.FLOOR_GENERAL for c in candidates):
        return None
    if majority(facts.lead):
        return [c for c in candidates if c.role == Role.FLOOR_GENERAL]
    return [c for c in candidates if c.role != Role.FLOOR_GENERAL]


def tb_interior(candidates, facts, three_season):
    """2. Teammates (interior): inside mojood ho aur koi big-family role candidate ho."""
    if facts.inside is None:
        return None
    if not any(family_for_role(c.role) == Family.BIGS for c in candidates):
        return None
    if majority(facts.inside):
        return [c for c in candidates if family_for_role(c.role) == Family.BIGS]
    # 50% se kam: non-big roles + Traditional Forward
    return [c for c in candidates
            if family_for_role(c.role) != Family.BIGS or c.role == Role.TRADITIONAL_FORWARD]


def tb_length(candidates, facts, three_season):
    """3. Length: wing roles sirf 6'5"+, guard roles sirf 6'5" se chhote (Floor General exempt)."""
    if facts.height is None:
        return None
    kept = []
    for c in candidates:
        if c.role in WING_ROLES and facts.height < H_6_5:
            continue
        if c.role in GUARD_ROLES and c.role != Role.FLOOR_GENERAL and facts.height >= H_6_5:
            continue
        kept.append(c)
    return kept


def tb_larger_sample(candidates, facts, three_season):
    """
    4. Larger sample: candidates alag families se hon aur 3-season read mojood ho.
    Jin candidates ke group ka 3-season score sab se ooncha ho, woh bachte hain.
    Sab ek hi family ke hon to "this season stands" (lagu nahi).
    """
    if three_season is None:
        return None
    families = {family_for_role(c.role) for c in candidates}
    if len(families) < 2:
        return None
    score_of = {c.group: three_season.get(c.group) for c in candidates}
    present = [s for s in score_of.values() if s is not None]
    if not present:
        return None
    best = max(present)
    return [c for c in candidates if score_of[c.group] == best]


def tb_higher_volume(candidates, facts, three_season):
    """5. Higher volume: is season ka ooncha score (pehla, agar barabar)."""
    best = max(c.score for c in candidates)
    return [next(c for c in candidates if c.score == best)]


TIEBREAKERS = (
    (DecidedBy.TB_CREATOR, tb_creator),
    (DecidedBy.TB_INTERIOR, tb_interior),
    (DecidedBy.TB_LENGTH, tb_length),
    (DecidedBy.TB_LARGER_SAMPLE, tb_larger_sample),
    (DecidedBy.TB_HIGHER_VOLUME, tb_higher_volume),
)


def run_tiebreakers(candidates, facts, three_season):
    """Order mein tiebreakers; (bacha hua candidate, kis ne faisla kiya)."""
    for name, tiebreaker in TIEBREAKERS:
        if len(candidates) < 2:
            break
        kept = tiebreaker(candidates, facts, three_season)
        # Sirf tab lagu: kam az kam ek hataye, kam az kam ek bachaye
        if kept is None or len(kept) == 0 or len(kept) == len(candidates):
            continue
        candidates = kept
        if len(candidates) == 1:
            return candidates[0], name
    # Kabhi yahan nahi aana chahiye (higher volume hamesha ek chhorta hai)
    return candidates[0], DecidedBy.TB_HIGHER_VOLUME


# ---------------------------------------------------------------------------
# Poora faisla
# ---------------------------------------------------------------------------

def decide_role(group_scores, facts, three_season=None):
    """
    group_scores: {Group: (raw, score)}  (R5)
    facts:        rules.PlayerFacts
    three_season: {Group: score} 3-season sample se, ya None (read nahi)

    Wapas: Decision, ya None agar koi proposal hi na bani.
    """
    proposals = make_proposals(group_scores, facts)

    # Stage D: guardrails
    for p in proposals:
        p.dropped_by_guardrail = breaks_guardrail(p.role, facts.height)
    ranked = sorted((p for p in proposals if not p.dropped_by_guardrail),
                    key=lambda p: p.score, reverse=True)
    if not ranked:
        return None

    # Stage E: top aur close calls
    top = ranked[0]
    close = [p for p in ranked[1:] if top.score - p.score <= DEF_CLOSE and p.role != top.role]

    if close:
        pick, decided_by = run_tiebreakers([top] + close, facts, three_season)
    else:
        pick, decided_by = top, DecidedBy.CLEAR_TOP_GROUP

    # Secondary: sab se oonchi proposal jis ka role pick se alag ho
    secondary = next((p.role for p in ranked if p.role != pick.role), None)

    return Decision(
        primary=pick.role,
        secondary=secondary,
        family=family_for_role(pick.role),
        winning_group=pick.group,
        decided_by=decided_by,
        proposals=proposals,
    )
