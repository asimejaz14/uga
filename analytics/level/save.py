"""
Level ko database mein likhna: SeasonLevelValues (1 row) + PlayerSeasonLevel (har player).
Hisaab pipeline.py ka hai; ye file sirf likhti hai.
"""
from analytics.models import PlayerSeasonLevel, SeasonLevelValues

WRITE_BATCH = 5_000


def save_level_season(run, data):
    league, ppw, rep = data.league, data.ppw, data.replacement

    SeasonLevelValues.objects.create(
        run=run,
        league_ft_pct=league.league_ft_pct,
        league_ppp=None,
        xpts_rim=league.xpts["rim"],
        xpts_mid=league.xpts["mid"],
        xpts_three=league.xpts["three"],
        ast_share_jumper=league.ast_share_jumper,
        d1_teams=data.d1_teams,
        ppw_teams=ppw.teams,
        ppw_intercept=ppw.intercept,
        ppw_slope=ppw.slope,
        ppw_r=ppw.r,
        points_per_win=ppw.points_per_win,
        bench_players=rep.bench_players,
        replacement_all=rep.overall,
        replacement_guards=rep.for_family("guards"),
        replacement_wings=rep.for_family("wings"),
        replacement_bigs=rep.for_family("bigs"),
    )

    rows = [
        PlayerSeasonLevel(
            run=run,
            player_id=p.player_id,
            team_id=p.team_id,
            role_placement_id=p.placement_id,
            family=p.family,
            minutes=p.minutes,
            coverage=p.coverage,
            epa_total=p.epa_total,
            epa_per40=p.epa_per40,
            surplus_per40=p.surplus_per40,
            war_per40=p.war_per40,
            war=p.war,
            tier=p.tier,
            is_d1=p.is_d1,
            is_rated=p.is_rated,
            is_qualified=p.is_qualified,
            history_complete=data.history_complete,
            **p.pieces,
        )
        for p in data.players.values()
    ]
    PlayerSeasonLevel.objects.bulk_create(rows, batch_size=WRITE_BATCH)
    return len(rows)
