"""
Steps 7-8 — from seven proposals to one role (spec 2.7 Stages D-F, and 2.8).

For each player:

  1. PROPOSALS   seven (group, role, group score) — from groups.py + rules.py
  2. GUARDRAILS  drop impossible proposals before ranking:
                   a big role   (UGA Big, Traditional Big)          needs 6'5" or taller
                   a guard role (Floor General, Combo Guard, Guard) needs 6'8" or under
                   no height -> passes both
  3. RANK        surviving proposals by group score, high to low. pick = the top one.
  4. CLOSE CALL  other proposals within 0.10 of the top whose ROLE is different.
                   none -> the top one wins             (decided_by = "clear")
                   some -> candidates = top + close ones -> tiebreakers
  5. TIEBREAKERS in order. Each one is used only if it removes at least one candidate
                 AND leaves at least one. The first that leaves a single role settles it.
                   1 creator        lead >= 50% -> only Floor General; < 50% -> drop Floor General
                   2 interior       inside >= 50% -> only big-family roles;
                                    < 50% -> non-big roles + Traditional Forward
                   3 length         wing roles only at 6'5"+; guard roles only under 6'5"
                                    (Floor General exempt); bigs untouched
                   4 larger_sample  candidates from different families + a three-season read:
                                    keep the one(s) whose group scores highest on 3 seasons
                   5 volume         keep the highest current group score
  6. OUTPUT      primary = winner, secondary = highest proposal with a different role,
                 family = Guards / Wings / Bigs read off the primary.

Players without a read (under 300 pooled possessions) should get the "matrix fit".
The spec does not define it, so for now they go through the same rules and are
flagged fallback=True, confidence=low, decided_by="fallback". Replace this when the
matrix fit is known.
"""
import pandas as pd

from .groups import GROUP_NAMES
from .rules import (COMBO_GUARD, FAMILY, FLOOR_GENERAL, GUARD, TRAD_BIG, TRAD_FORWARD,
                    UGA_BIG, Rules, missing)

BIG_ROLES = {UGA_BIG, TRAD_BIG}                      # for the guardrail
GUARD_ROLES = {FLOOR_GENERAL, COMBO_GUARD, GUARD}    # for the guardrail


# ---------------------------------------------------------------------------
# 2. guardrails
# ---------------------------------------------------------------------------

def passes_guardrails(role, height, c):
    if missing(height):
        return True
    if role in BIG_ROLES and height < c["H_WING"]:
        return False
    if role in GUARD_ROLES and height > c["H_GUARD_MAX"]:
        return False
    return True


# ---------------------------------------------------------------------------
# 5. tiebreakers — each returns the candidates it would KEEP, or None if it
#    does not apply. A candidate is a dict: {"group", "role", "score"}.
# ---------------------------------------------------------------------------

def tb_creator(cands, p, three, c):
    roles = {x["role"] for x in cands}
    if missing(p["lead"]) or FLOOR_GENERAL not in roles:
        return None
    if p["lead"] >= c["SHARE_THRESHOLD"]:
        return [x for x in cands if x["role"] == FLOOR_GENERAL]
    return [x for x in cands if x["role"] != FLOOR_GENERAL]


def tb_interior(cands, p, three, c):
    has_big = any(FAMILY[x["role"]] == "Bigs" for x in cands)
    if len(cands) < 2 or missing(p["inside"]) or not has_big:
        return None
    if p["inside"] >= c["SHARE_THRESHOLD"]:
        return [x for x in cands if FAMILY[x["role"]] == "Bigs"]
    return [x for x in cands if FAMILY[x["role"]] != "Bigs" or x["role"] == TRAD_FORWARD]


def tb_length(cands, p, three, c):
    h = p["height_in"]
    if len(cands) < 2 or missing(h):
        return None
    keep = []
    for x in cands:
        family = FAMILY[x["role"]]
        if family == "Wings" and h < c["H_WING"]:
            continue                       # wing roles need 6'5"+
        if family == "Guards" and x["role"] != FLOOR_GENERAL and h >= c["H_WING"]:
            continue                       # guard roles need under 6'5" (FG exempt)
        keep.append(x)
    return keep


def tb_larger_sample(cands, p, three, c):
    families = {FAMILY[x["role"]] for x in cands}
    if len(cands) < 2 or len(families) < 2 or three is None:
        return None                        # same family: this season stands
    score3 = {x["group"]: three.get(x["group"]) for x in cands}
    score3 = {g: (-1.0 if missing(s) else s) for g, s in score3.items()}
    best = max(score3.values())
    return [x for x in cands if score3[x["group"]] == best]


def tb_volume(cands, p, three, c):
    best = max(x["score"] for x in cands)
    return [x for x in cands if x["score"] == best]


TIEBREAKERS = [("creator", tb_creator), ("interior", tb_interior), ("length", tb_length),
               ("larger_sample", tb_larger_sample), ("volume", tb_volume)]


def run_tiebreakers(cands, p, three, c):
    """Apply the tiebreakers in order. Returns (winning candidate, tiebreaker name)."""
    for name, rule in TIEBREAKERS:
        kept = rule(cands, p, three, c)
        if kept is None:
            continue                                     # does not apply
        if 0 < len(kept) < len(cands):                   # removes some, leaves some
            cands = kept
        if len({x["role"] for x in cands}) == 1:         # one role left: settled
            return cands[0], name
    # Still a tie after volume (two equal scores): take the first, still "volume".
    return cands[0], "volume"


# ---------------------------------------------------------------------------
# One player
# ---------------------------------------------------------------------------

def place_player(proposals, p, three, c):
    """proposals: list of {"group", "role", "score"} for the seven groups.
    p:         the player dict used by the rules (height_in, lead, inside, ...)
    three:     {group: three-season group score}, or None if no three-season read

    Returns a dict: primary, secondary, winning_group, decided_by, ranked
    """
    scored = [x for x in proposals if not missing(x["score"])]

    # 2. guardrails
    surviving = [x for x in scored if passes_guardrails(x["role"], p["height_in"], c)]
    if not surviving:                     # should not happen; keep the player placeable
        surviving = scored

    # 3. rank (ties keep the spec's group order, because sorted() is stable)
    ranked = sorted(surviving, key=lambda x: -x["score"])
    top = ranked[0]

    # 4. close call?
    close = [x for x in ranked[1:]
             if top["score"] - x["score"] <= c["DEF_CLOSE"] and x["role"] != top["role"]]
    if close:
        winner, decided_by = run_tiebreakers([top] + close, p, three, c)
    else:
        winner, decided_by = top, "clear"

    # 6. secondary = highest proposal whose role differs from the primary
    secondary = next((x["role"] for x in ranked if x["role"] != winner["role"]), None)

    return dict(primary=winner["role"], secondary=secondary, winning_group=winner["group"],
                decided_by=decided_by, ranked=ranked)


# ---------------------------------------------------------------------------
# Every player in a season
# ---------------------------------------------------------------------------

def _row_or_blank(df, pid, col):
    return df.at[pid, col] if pid in df.index and col in df.columns else float("nan")


def compute_placements(pooled, play_types, groups, groups3, play_types3, shares, mode, c):
    """Main entry point for Steps 6b-8.

    Returns (placements, proposals):
      placements  one row per player, ready for RolePlacement
      proposals   one row per player x group with the proposed role, for PlayerGroupScore
    """
    rules = Rules(c)
    pooled = pooled.set_index("player_id")
    pt = play_types.set_index("player_id")
    gs = groups.set_index("player_id")
    gs3 = groups3.set_index("player_id")
    read3 = play_types3.set_index("player_id")["read"]
    sh = shares.set_index("player_id") if len(shares) else pd.DataFrame()

    usage_median = pooled.loc[pooled["qualified"].astype(bool), "usage"].median()
    pctl_cols = [col for col in pt.columns if col.startswith("pctl_")]

    placements, proposal_rows = [], []
    for pid in pooled.index:
        # --- everything the rules need about this player, in one dict ---------
        p = {
            "height_in": pooled.at[pid, "height_in"],
            "three_pa_share": pooled.at[pid, "three_pa_share"],
            "usage": pooled.at[pid, "usage"],
            "usage_median": usage_median,
            "raw_shooting": gs.at[pid, "raw_shooting"],
            "pctl_drb": pt.at[pid, "pctl_drb"],
            "pctl_blocks": pt.at[pid, "pctl_blocks"],
            "pctl_steals": pt.at[pid, "pctl_steals"],
        }
        for k in ["lead", "lead2", "inside", "inside2", "front"]:
            p[k] = _row_or_blank(sh, pid, k)

        # --- 1. seven proposals ---------------------------------------------------
        roles = rules.propose_all(p)
        proposals = [{"group": g, "role": roles[g], "score": gs.at[pid, f"score_{g}"]}
                     for g in GROUP_NAMES]
        for x in proposals:
            proposal_rows.append(dict(player_id=pid, group_name=x["group"],
                                      proposed_role=x["role"]))

        three = None
        if pid in gs3.index and bool(read3.get(pid, False)):
            three = {g: gs3.at[pid, f"score_{g}"] for g in GROUP_NAMES}

        # --- 2-6. guardrails, ranking, tiebreakers --------------------------------
        result = place_player(proposals, p, three, c)

        read = bool(pooled.at[pid, "read"])
        top4 = pt.loc[pid, pctl_cols].dropna().sort_values(ascending=False).head(4)
        placements.append(dict(
            player_id=int(pid),
            primary_role=result["primary"],
            secondary_role=result["secondary"],
            family=FAMILY[result["primary"]],
            confidence=pooled.at[pid, "confidence"],
            fallback=not read,
            rules_mode=mode,
            pooled_off_poss=int(round(pooled.at[pid, "off_poss"])),
            winning_group=result["winning_group"],
            top3_groups=[{"group": x["group"], "score": round(float(x["score"]), 4),
                          "role": x["role"]} for x in result["ranked"][:3]],
            decided_by=result["decided_by"] if read else "fallback",
            top4_play_types=[{"play_type": k.removeprefix("pctl_"), "pctl": round(float(v), 4)}
                             for k, v in top4.items()],
            lead=p["lead"],
            inside=p["inside"],
        ))
    return pd.DataFrame(placements), pd.DataFrame(proposal_rows)
