"""
Raw database (bball_raw) se basketball app ke models mein data laana.

Ye file sirf FUNCTIONS rakhti hai; `import_raw` management command inhein
sahi order mein bulati hai. Har function ek table (ya ek jora) import karta
hai aur kitni rows likhi gayin, woh wapas karta hai.

Do tareeqe (dekhein ASSUMPTIONS.md D-19):

  Dimension tables (Team, TeamSeason, Player, Game, NationalAssistShare):
      UPSERT: row hai to update, nahi to insert. Kabhi delete nahi, kyunke
      analytics ke results in ki taraf PROTECT FK rakhte hain.

  Fact tables (4 player-season tables, Possession):
      REPLACE PER SEASON: ek transaction mein us season ki rows delete,
      phir raw se nayi insert. Fail ho to delete bhi wapas (purana data salamat).

ESPN id -> Django id: har parent import ke baad ek IdMap banta hai.
Agar koi ESPN id na mile to MissingReferenceError aata hai aur import
ruk jata hai; chupke se ghalat data nahi jata.
"""
from django.db import connections, transaction

from .models import (
    Game, NationalAssistShare, Player, PlayerSeasonBox, PlayerSeasonCounts,
    PlayerSeasonPossessions, Possession, Team, TeamSeason, TorvikPlayerSeason,
)

RAW_DB = "raw"          # settings.DATABASES ki key
WRITE_BATCH = 5_000     # bulk_create ek dafa mein kitni rows likhe
FETCH_CHUNK = 10_000    # bari table se ek dafa mein kitni rows parhe


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class MissingReferenceError(Exception):
    """Raw data mein aisi ESPN id jis ka parent (team / player / game) mojood nahi."""


class IdMap:
    """
    ESPN id -> Django id ki dictionary, saaf error message ke saath.

        teams = IdMap.for_model(Team, "espn_team_id")
        teams.get(61)            # -> 1 (Django id); na mile to MissingReferenceError
        teams.get_optional(None) # -> None (nullable columns ke liye)
    """

    def __init__(self, mapping, label):
        self.mapping = mapping
        self.label = label

    @classmethod
    def for_model(cls, model, espn_field):
        mapping = dict(model.objects.values_list(espn_field, "id"))
        return cls(mapping, model.__name__)

    def get(self, espn_id, context=""):
        try:
            return self.mapping[espn_id]
        except KeyError:
            raise MissingReferenceError(
                f"{self.label} ESPN id {espn_id} nahi mili. {context}".strip()
            ) from None

    def get_optional(self, espn_id, context=""):
        """NULL ho to None; warna get() jaisa."""
        if espn_id is None:
            return None
        return self.get(espn_id, context)

    def __len__(self):
        return len(self.mapping)


def fetch_dicts(sql, params=None):
    """
    Raw DB se CHOTI query ke saare rows, har row ek dict.
    Bari tables (possessions) ke liye stream_dicts() use karein.
    """
    with connections[RAW_DB].cursor() as cur:
        cur.execute(sql, params)
        columns = [col[0] for col in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]


def stream_dicts(sql, params=None, chunk_size=FETCH_CHUNK):
    """
    Raw DB se BARI query ke rows, tukron (chunks) mein. Har chunk dicts ki list.

    chunked_cursor() Postgres par server-side cursor banata hai: result
    database mein rehta hai aur fetchmany() sirf chunk_size rows laata hai.
    Is liye 800k rows bhi memory mein ek saath nahi aatin.

    Note: psycopg2 ke server-side cursor mein `cur.description` execute() ke
    baad None hota hai; column names pehli fetchmany() ke baad milte hain.
    Is liye columns pehle chunk ke baad parhte hain (psycopg 3 par bhi chalta hai).
    """
    with connections[RAW_DB].chunked_cursor() as cur:
        cur.execute(sql, params)
        columns = None
        while True:
            rows = cur.fetchmany(chunk_size)
            if not rows:
                break
            if columns is None:
                columns = [col[0] for col in cur.description]
            yield [dict(zip(columns, row)) for row in rows]


def raw_seasons(raw_table):
    """Raw table mein kaunse seasons hain (jaise [2024, 2025, 2026])."""
    rows = fetch_dicts(f"SELECT DISTINCT season FROM {raw_table} ORDER BY season")
    return [r["season"] for r in rows]


# ---------------------------------------------------------------------------
# Dimension tables (upsert)
# ---------------------------------------------------------------------------

def import_teams():
    """
    Team aur TeamSeason.

    Raw `teams` mein har season ki alag row hai. Team.name sab se naye
    season ka naam leta hai (DISTINCT ON + season DESC).
    """
    latest_names = fetch_dicts(
        """
        SELECT DISTINCT ON (team_id) team_id, team_name
        FROM teams
        ORDER BY team_id, season DESC
        """
    )
    Team.objects.bulk_create(
        [Team(espn_team_id=r["team_id"], name=r["team_name"]) for r in latest_names],
        update_conflicts=True,
        unique_fields=["espn_team_id"],
        update_fields=["name"],
        batch_size=WRITE_BATCH,
    )

    teams = IdMap.for_model(Team, "espn_team_id")
    season_rows = fetch_dicts("SELECT team_id, season, conference_id FROM teams")
    TeamSeason.objects.bulk_create(
        [
            TeamSeason(
                team_id=teams.get(r["team_id"]),
                season=r["season"],
                conference_id=r["conference_id"],
            )
            for r in season_rows
        ],
        update_conflicts=True,
        unique_fields=["team", "season"],
        update_fields=["conference_id"],
        batch_size=WRITE_BATCH,
    )
    return {"Team": len(latest_names), "TeamSeason": len(season_rows)}


def import_players():
    """Player (raw `players`)."""
    rows = fetch_dicts("SELECT player_id, player_name FROM players")
    Player.objects.bulk_create(
        [Player(espn_player_id=r["player_id"], name=r["player_name"]) for r in rows],
        update_conflicts=True,
        unique_fields=["espn_player_id"],
        update_fields=["name"],
        batch_size=WRITE_BATCH,
    )
    return {"Player": len(rows)}


GAME_UPDATE_FIELDS = [
    "season", "game_date", "home_team", "away_team", "season_type",
    "tournament_id", "has_shot_tags", "is_completed", "home_score", "away_score",
]


def import_games():
    """
    Game (raw `games`). SAARE games aate hain, postseason aur tournaments bhi;
    filter calculation ke waqt Game.objects.regular_season() se lagta hai (D-14).
    """
    teams = IdMap.for_model(Team, "espn_team_id")
    rows = fetch_dicts(
        """
        SELECT game_id, season, game_date, home_team_id, away_team_id, season_type,
               tournament_id, has_shot_tags, is_completed, home_score, away_score
        FROM games
        """
    )
    objs = []
    for r in rows:
        context = f"(game {r['game_id']})"
        objs.append(
            Game(
                espn_game_id=r["game_id"],
                season=r["season"],
                game_date=r["game_date"],
                home_team_id=teams.get(r["home_team_id"], context),
                away_team_id=teams.get(r["away_team_id"], context),
                season_type=r["season_type"],
                tournament_id=r["tournament_id"],
                has_shot_tags=r["has_shot_tags"],
                is_completed=r["is_completed"],
                home_score=r["home_score"],
                away_score=r["away_score"],
            )
        )
    Game.objects.bulk_create(
        objs,
        update_conflicts=True,
        unique_fields=["espn_game_id"],
        update_fields=GAME_UPDATE_FIELDS,
        batch_size=WRITE_BATCH,
    )
    return {"Game": len(objs)}


def import_national_assist_share():
    """NationalAssistShare (raw `national_assist_share`)."""
    rows = fetch_dicts("SELECT season, zone, ast_share FROM national_assist_share")
    NationalAssistShare.objects.bulk_create(
        [NationalAssistShare(season=r["season"], zone=r["zone"], ast_share=r["ast_share"]) for r in rows],
        update_conflicts=True,
        unique_fields=["season", "zone"],
        update_fields=["ast_share"],
        batch_size=WRITE_BATCH,
    )
    return {"NationalAssistShare": len(rows)}


# ---------------------------------------------------------------------------
# Fact tables (replace per season)
# ---------------------------------------------------------------------------

# Django model -> raw table ka naam. In charon models ke field names raw
# columns jaise hi rakhe gaye hain, is liye columns ki list model se nikalti hai.
PLAYER_SEASON_TABLES = {
    PlayerSeasonCounts: "player_season_counts",
    PlayerSeasonPossessions: "player_season_possessions",
    PlayerSeasonBox: "player_season_box",
    TorvikPlayerSeason: "torvik_player_season",
}

# Ye fields alag se handle hoti hain (mapping ya Django ki apni).
_SPECIAL_FIELDS = {"id", "player", "team", "season"}


def data_columns(model):
    """
    Model ke woh fields jo raw se seedhe copy hote hain.
    Jaise PlayerSeasonBox -> ["minutes", "points"].

    Model mein naya field add hua aur raw mein woh column nahi, to SQL foran
    error dega ("column does not exist"). Is tarah model aur raw kabhi
    chupke se alag nahi ho sakte.
    """
    return [f.name for f in model._meta.concrete_fields if f.name not in _SPECIAL_FIELDS]


def import_player_season_table(model, seasons=None):
    """
    Ek player-season table, season by season: delete + insert ek transaction mein.

    seasons=None ka matlab: raw table ke saare seasons.
    """
    raw_table = PLAYER_SEASON_TABLES[model]
    columns = data_columns(model)
    players = IdMap.for_model(Player, "espn_player_id")
    teams = IdMap.for_model(Team, "espn_team_id")

    if seasons is None:
        seasons = raw_seasons(raw_table)

    total = 0
    for season in seasons:
        rows = fetch_dicts(
            f"SELECT player_id, team_id, {', '.join(columns)} FROM {raw_table} WHERE season = %s",
            [season],
        )
        objs = []
        for r in rows:
            context = f"({raw_table}, season {season})"
            objs.append(
                model(
                    player_id=players.get(r["player_id"], context),
                    team_id=teams.get(r["team_id"], context),
                    season=season,
                    **{col: r[col] for col in columns},
                )
            )
        with transaction.atomic():
            model.objects.filter(season=season).delete()
            model.objects.bulk_create(objs, batch_size=WRITE_BATCH)
        total += len(objs)
    return {model.__name__: total}


POSSESSION_SQL = """
    SELECT game_id, possession_no, off_team_id, def_team_id,
           off_p1, off_p2, off_p3, off_p4, off_p5,
           def_p1, def_p2, def_p3, def_p4, def_p5,
           garbage_time, off_five_distinct, def_five_distinct
    FROM possessions
    WHERE season = %s
"""

PLAYER_SLOTS = (
    "off_p1", "off_p2", "off_p3", "off_p4", "off_p5",
    "def_p1", "def_p2", "def_p3", "def_p4", "def_p5",
)


def import_possessions(seasons=None, progress=None):
    """
    Possession (raw `possessions`, ~2.36M rows). Season by season, streaming.

    Har season ek transaction hai: purani rows delete, nayi rows chunks mein
    insert. Beech mein fail ho to poori season wapas (purana data salamat).

    progress: optional function(season, rows_so_far), command progress print
    karne ke liye deti hai.
    """
    games = IdMap.for_model(Game, "espn_game_id")
    teams = IdMap.for_model(Team, "espn_team_id")
    players = IdMap.for_model(Player, "espn_player_id")

    if seasons is None:
        seasons = raw_seasons("possessions")

    total = 0
    for season in seasons:
        season_count = 0
        with transaction.atomic():
            Possession.objects.filter(season=season).delete()
            for chunk in stream_dicts(POSSESSION_SQL, [season]):
                objs = []
                for r in chunk:
                    context = f"(possession game {r['game_id']} #{r['possession_no']})"
                    player_kwargs = {
                        f"{slot}_id": players.get_optional(r[slot], context)
                        for slot in PLAYER_SLOTS
                    }
                    objs.append(
                        Possession(
                            game_id=games.get(r["game_id"], context),
                            possession_no=r["possession_no"],
                            season=season,
                            off_team_id=teams.get(r["off_team_id"], context),
                            def_team_id=teams.get(r["def_team_id"], context),
                            garbage_time=r["garbage_time"],
                            off_five_distinct=r["off_five_distinct"],
                            def_five_distinct=r["def_five_distinct"],
                            **player_kwargs,
                        )
                    )
                Possession.objects.bulk_create(objs, batch_size=WRITE_BATCH)
                season_count += len(objs)
                if progress:
                    progress(season, season_count)
        total += season_count
    return {"Possession": total}