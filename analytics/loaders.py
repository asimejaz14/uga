"""
Database se calculations ke liye plain data laana (D-13).

Calculation files (analytics/level/, analytics/role/) Django models ko
nahi chhuti; unhein data yahan se dataclasses / dicts ki shakal mein milta hai.
Is tarah "data kahan se aaya" aur "us par kya hisaab hua" alag rehte hain.
"""
from collections import defaultdict

from django.db.models import Sum

from analytics.choices import RulesMode
from collections import Counter

from basketball.models import (
    Game, NationalAssistShare, PlayerSeasonBox, PlayerSeasonCounts, PlayerSeasonPossessions,
    Possession, TeamSeason, TorvikPlayerSeason,
)

from .level.league import LeagueShotTotals, TeamRecord


def league_shot_totals(season):
    """
    Season ke SAB players ke shot counts ka jama.
    Population = all (Q-06; D1-only spec se kaafi door tha).
    """
    fields = ["fga_rim", "fgm_rim", "fga_mid", "fgm_mid", "fga_three", "fgm_three", "fta", "ftm"]
    sums = PlayerSeasonCounts.objects.filter(season=season).aggregate(
        **{name: Sum(name) for name in fields}
    )
    if sums["fga_rim"] is None:
        raise ValueError(f"Season {season} ke counts nahi mile.")
    return LeagueShotTotals(**sums)


def national_assist_shares(season):
    """{"rim": 0.4262, "mid": 0.2648, "three": 0.8318} (data engineer ki table, as-is)."""
    return {
        row["zone"]: float(row["ast_share"])
        for row in NationalAssistShare.objects.filter(season=season).values("zone", "ast_share")
    }


def d1_team_records(season):
    """
    Har D1 team ka regular-season record (Game.objects.regular_season(), D-14).
    D1 teams ke SAARE regular games ginte hain, non-D1 opponents ke khilaf bhi
    (V-17 isi tarah exact match hua). 10+ games ka filter league.py mein hai.
    """
    d1_team_ids = set(
        TeamSeason.objects.filter(season=season, conference_id__isnull=False)
        .values_list("team_id", flat=True)
    )

    games = defaultdict(int)
    wins = defaultdict(int)
    margin = defaultdict(int)

    rows = (
        Game.objects.regular_season()
        .filter(season=season, home_score__isnull=False, away_score__isnull=False)
        .values_list("home_team_id", "away_team_id", "home_score", "away_score")
    )
    for home, away, home_score, away_score in rows:
        for team, scored, allowed in ((home, home_score, away_score), (away, away_score, home_score)):
            if team not in d1_team_ids:
                continue
            games[team] += 1
            wins[team] += int(scored > allowed)
            margin[team] += scored - allowed

    return [
        TeamRecord(team_id=t, games=games[t], wins=wins[t], point_margin=margin[t])
        for t in games
    ]


# ---------------------------------------------------------------------------
# Role
# ---------------------------------------------------------------------------

def d1_team_ids(season):
    """Is season ki D1 teams ke Django ids (conference id wali)."""
    return set(
        TeamSeason.objects.filter(season=season, conference_id__isnull=False)
        .values_list("team_id", flat=True)
    )


def role_frame(season):
    """
    Jin players ko Role dena hai (A-17): is season counts ki row hai aur
    team D1 hai. Spec ka "players in frame" (2026: 4,978).
    Wapas: player ids ki sorted list.
    """
    d1_teams = d1_team_ids(season)
    return sorted(
        PlayerSeasonCounts.objects.filter(season=season, team_id__in=d1_teams)
        .values_list("player_id", flat=True)
    )


def off_possessions_lookup(player_ids, seasons):
    """
    {(player_id, season): off_poss} un players aur seasons ke liye.
    Jis player-season ki row nahi, woh dict mein nahi hoga.
    """
    rows = PlayerSeasonPossessions.objects.filter(
        player_id__in=player_ids, season__in=seasons
    ).values_list("player_id", "season", "off_poss")
    return {(player_id, season): off_poss for player_id, season, off_poss in rows}


def seasons_in_data():
    """Database mein kaunse seasons ke possessions hain, jaise {2024, 2025, 2026}."""
    return set(PlayerSeasonPossessions.objects.values_list("season", flat=True).distinct())


def rules_mode_for_season(season):
    """
    FULL agar is season ke regular games mein shot tags hain (2026), warna COARSE.
    Saal hard-code nahi (D-12): production mein bhi data hi batata hai.
    """
    has_tags = Game.objects.regular_season().filter(season=season, has_shot_tags=True).exists()
    return RulesMode.FULL if has_tags else RulesMode.COARSE


# PlayerSeasonCounts ke woh columns jo Role ko chahiyein
_ROLE_COUNT_FIELDS = (
    "assists", "ast_to_three", "ast_to_rim", "ft_trips", "transition_fga",
    "steals", "blocks", "drb", "orb", "putbacks",
    "fga_rim", "fgm_rim", "fgm_rim_ast", "fga_mid", "fgm_mid", "fgm_mid_ast",
    "fga_three", "fgm_three", "fgm_three_ast",
    "driving_layups", "pullups_2", "pullup_range_2s", "floaters", "pullups_3",
    "plain_rim_fga", "plain_rim_fgm", "plain_rim_fgm_ast", "tip_ins", "hooks_turnarounds",
)


# Tagged aur current-only columns (counts row na ho to None, 0 nahi)
_CURRENT_ONLY_COUNT_FIELDS = (
    "driving_layups", "pullups_2", "pullup_range_2s", "floaters", "pullups_3",
    "plain_rim_fga", "plain_rim_fgm", "plain_rim_fgm_ast", "tip_ins", "hooks_turnarounds",
)


def role_rows_lookup(player_ids, seasons):
    """
    {(player_id, season): row} jahan row = counts + possessions ek dict mein.

    Har woh player-season shamil hai jis ki counts YA possessions ki row ho:
      - possessions hain, counts nahi -> counts 0 (khela, lekin koi event nahi);
        tagged columns None
      - counts hain, possessions nahi -> off_poss/def_poss 0, tagged_off_poss None
    Is tarah R1 (possessions) aur R2/R3 (counts) ek hi data dekhte hain.
    """
    possessions = {
        (pid, season): (off, deff, tagged)
        for pid, season, off, deff, tagged in PlayerSeasonPossessions.objects.filter(
            player_id__in=player_ids, season__in=seasons
        ).values_list("player_id", "season", "off_poss", "def_poss", "tagged_off_poss")
    }
    counts = {}
    for row in PlayerSeasonCounts.objects.filter(
        player_id__in=player_ids, season__in=seasons
    ).values("player_id", "season", *_ROLE_COUNT_FIELDS):
        counts[(row.pop("player_id"), row.pop("season"))] = row

    rows = {}
    for key in set(possessions) | set(counts):
        row = counts.get(key)
        if row is None:
            # Koi counts row nahi: base counts 0, tagged/current-only None
            row = {field: (None if field in _CURRENT_ONLY_COUNT_FIELDS else 0)
                   for field in _ROLE_COUNT_FIELDS}
        off, deff, tagged = possessions.get(key, (0, 0, None))
        rows[key] = {**row, "off_poss": off, "def_poss": deff, "tagged_off_poss": tagged}
    return rows


def qualified_player_ids(season, frame_player_ids):
    """
    Spec ka "qualified" (percentiles ki population): Torvik minutes% >= 40
    aur IS season 300+ offensive possessions. (2026 spec: 2,284.)
    """
    from analytics.constants import MIN_READ_POSS, QUALIFIED_MIN_PCT

    min_pct_ok = set(
        TorvikPlayerSeason.objects.filter(
            season=season, player_id__in=frame_player_ids, min_pct__gte=QUALIFIED_MIN_PCT
        ).values_list("player_id", flat=True)
    )
    poss_ok = set(
        PlayerSeasonPossessions.objects.filter(
            season=season, player_id__in=frame_player_ids, off_poss__gte=MIN_READ_POSS
        ).values_list("player_id", flat=True)
    )
    return min_pct_ok & poss_ok


def offensive_lineup_counts(season):
    """
    {(p1, p2, p3, p4, p5): kitni possessions} is season ke liye.

    Sirf woh offensive possessions jo spec ke mutabiq ginti hain:
    5 distinct players aur garbage time nahi (Possession.counts_for_offense).
    Lineup ke ids sort kiye jate hain, taake same 5 players hamesha ek hi key bane.
    ~800k rows ek dafa parhi jati hain (iterator: memory mein tukron mein).
    """
    lineups = Counter()
    rows = (
        Possession.objects.filter(season=season, off_five_distinct=True, garbage_time=False)
        .values_list("off_p1_id", "off_p2_id", "off_p3_id", "off_p4_id", "off_p5_id")
        .iterator(chunk_size=20_000)
    )
    for row in rows:
        if None in row:
            continue
        lineups[tuple(sorted(row))] += 1
    return lineups


def heights(season, player_ids):
    """{player_id: height in inches (float)} Torvik se; jin ki height nahi woh dict mein nahi."""
    return {
        pid: float(h)
        for pid, h in TorvikPlayerSeason.objects.filter(
            season=season, player_id__in=player_ids, height_in__isnull=False
        ).values_list("player_id", "height_in")
    }


def torvik_role_values(season, player_ids):
    """{player_id: (usage, three_pa_share)} Torvik se, floats mein."""
    return {
        pid: (float(usage), float(share))
        for pid, usage, share in TorvikPlayerSeason.objects.filter(
            season=season, player_id__in=player_ids
        ).values_list("player_id", "usage", "three_pa_share")
    }



# ---------------------------------------------------------------------------
# Level
# ---------------------------------------------------------------------------

_LEVEL_COUNT_FIELDS = (
    "fga_rim", "fgm_rim", "fgm_rim_ast", "fga_mid", "fgm_mid", "fgm_mid_ast",
    "fga_three", "fgm_three", "fgm_three_ast", "fta", "ftm",
    "assists", "ast_to_rim", "ast_to_three", "turnovers", "orb", "steals", "blocks",
    "fts_conceded", "technicals",
)


def level_rows(season):
    """
    Level ke liye har player ki ek row: box (minutes, points, team) + counts.

    Sirf woh players jin ki box AUR counts dono rows hain (A-29: counts ke
    baghair EPA nahi ban sakta). Wapas: list of dicts.
    """
    counts = {
        row.pop("player_id"): row
        for row in PlayerSeasonCounts.objects.filter(season=season).values("player_id", *_LEVEL_COUNT_FIELDS)
    }
    d1_teams = d1_team_ids(season)
    rows = []
    for player_id, team_id, minutes, points in PlayerSeasonBox.objects.filter(season=season).values_list(
        "player_id", "team_id", "minutes", "points"
    ):
        if player_id not in counts:
            continue
        rows.append({
            "player_id": player_id, "team_id": team_id, "minutes": minutes, "points": points,
            "is_d1": team_id in d1_teams, "counts": counts[player_id],
        })
    return rows


def role_families(season):
    """
    Is season ki latest SUCCESS Role run se {player_id: (placement_id, family)}.
    Role run na ho to (None, {}).
    """
    from analytics.choices import RunKind
    from analytics.models import CalculationRun, RolePlacement

    run = CalculationRun.objects.latest_success(RunKind.ROLE, season)
    if run is None:
        return None, {}
    families = {
        player_id: (placement_id, family)
        for placement_id, player_id, family in RolePlacement.objects.filter(run=run).values_list(
            "id", "player_id", "family"
        )
    }
    return run, families


def seasons_with_counts():
    """Database mein kaunse seasons ke counts hain (Level ko yahi chahiye)."""
    return set(PlayerSeasonCounts.objects.values_list("season", flat=True).distinct())
