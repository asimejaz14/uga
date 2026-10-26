"""
Role step R10: pipeline ka natija database mein likhna.

    CalculationRun (kind=role)  ->  RolePlacement (har frame player)
                                ->  GroupScore (har placement ke 7 groups x 2 samples)

Ye file database mein LIKHTI hai; hisaab kuch nahi karti. Saara hisaab
pipeline.py ka hai.
"""
from collections import Counter

from analytics.choices import Confidence, DecidedBy, Sample
from analytics.models import GroupScore, RolePlacement
from analytics.role import pooling
from analytics.role.percentiles import top_play_types

WRITE_BATCH = 5_000


def placement_for(run, data, player_id):
    """Ek player ki RolePlacement (abhi save nahi)."""
    result = data.pooling[player_id]
    decision = data.decisions.get(player_id)
    shares = data.shares.get(player_id)
    groups = data.groups.get(player_id, {})

    top3 = sorted(
        ((g, score) for g, (_, score) in groups.items() if score is not None),
        key=lambda item: item[1], reverse=True,
    )[:3]

    return RolePlacement(
        run=run,
        player_id=player_id,
        primary_role=decision.primary if decision else None,
        secondary_role=decision.secondary if decision else None,
        family=decision.family if decision else None,
        confidence=result.confidence if decision else Confidence.LOW,
        fallback=result.fallback,
        rules_mode=data.rules_mode,
        history_complete=result.history_complete,
        is_qualified=player_id in data.qualified,
        pooled_off_poss=round(result.pooled_off_poss),
        winning_group=decision.winning_group if decision else None,
        decided_by=decision.decided_by if decision else DecidedBy.NO_DATA,
        top3_groups=[{"group": str(g), "score": round(s, 4)} for g, s in top3],
        top4_play_types=top_play_types(data.percentiles.get(player_id, {})),
        lead=shares.lead if shares else None,
        lead2=shares.lead2 if shares else None,
        inside=shares.inside if shares else None,
        inside2=shares.inside2 if shares else None,
        front=shares.front if shares else None,
        shares_valid_poss=shares.valid_poss if shares else None,
    )


def group_scores_for(placement, data):
    """Ek placement ki GroupScore rows: current (proposal ke saath) + three_season."""
    player_id = placement.player_id
    decision = data.decisions.get(player_id)
    proposal_of = {p.group: p for p in (decision.proposals if decision else [])}

    rows = []
    for group, (raw, score) in data.groups.get(player_id, {}).items():
        proposal = proposal_of.get(group)
        rows.append(GroupScore(
            placement=placement, group=group, sample=Sample.CURRENT,
            raw_score=raw, group_score=score,
            proposed_role=proposal.role if proposal else None,
            dropped_by_guardrail=proposal.dropped_by_guardrail if proposal else False,
        ))
    for group, (raw, score) in data.three_season_groups.get(player_id, {}).items():
        rows.append(GroupScore(
            placement=placement, group=group, sample=Sample.THREE_SEASON,
            raw_score=raw, group_score=score,
        ))
    return rows


def save_role_season(run, data):
    """
    Saari placements aur group scores likho. Transaction command ki zimmedari hai.
    Wapas: run.summary ke liye khulasa (dict).
    """
    placements = [placement_for(run, data, p) for p in data.frame]
    # Postgres bulk_create ke baad har object ka id set kar deta hai
    RolePlacement.objects.bulk_create(placements, batch_size=WRITE_BATCH)

    group_rows = []
    for placement in placements:
        group_rows.extend(group_scores_for(placement, data))
    GroupScore.objects.bulk_create(group_rows, batch_size=WRITE_BATCH)

    qualified = [p for p in placements if p.is_qualified and p.primary_role]
    return {
        "frame": len(placements),
        "qualified": len(data.qualified),
        "usage_median": data.usage_median,
        "pooling": dict(Counter(r.status for r in data.pooling.values())),
        "decided_by": dict(Counter(str(p.decided_by) for p in placements)),
        "qualified_roles": dict(Counter(str(p.primary_role) for p in qualified)),
        "group_score_rows": len(group_rows),
        "no_data": sum(1 for r in data.pooling.values() if r.status == pooling.NO_DATA),
    }
