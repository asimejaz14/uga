"""
Raw database (bball_raw) se basketball models mein data import.

Istemal:
    python manage.py import_raw                       # sab kuch, saare seasons
    python manage.py import_raw --season 2026         # fact tables sirf 2026
    python manage.py import_raw --season 2025 --season 2026
    python manage.py import_raw --skip-possessions    # possessions chhor do (tez, dev ke liye)

Dimension tables (teams, players, games, national share) HAMESHA poori
upsert hoti hain, --season sirf fact tables par lagta hai.

Command dobara chalana mehfooz hai (idempotent): rows duplicate nahi hoti.
"""
import time

from django.core.management.base import BaseCommand, CommandError

from basketball import importers
from basketball.models import (
    Game, NationalAssistShare, Player, PlayerSeasonBox, PlayerSeasonCounts,
    PlayerSeasonPossessions, Possession, Team, TeamSeason, TorvikPlayerSeason,
)


class Command(BaseCommand):
    help = "data_duml_final database se basketball app ke models mein data import karta hai."

    def add_arguments(self, parser):
        parser.add_argument(
            "--season",
            type=int,
            action="append",
            dest="seasons",
            help="Sirf ye season(s) ki fact tables. Kai dafa de sakte hain. Na dein to saare seasons.",
        )
        parser.add_argument(
            "--skip-possessions",
            action="store_true",
            help="Possession table import na karo (sab se bari table).",
        )

    def handle(self, *args, **options):
        seasons = options["seasons"]
        started = time.monotonic()

        try:
            # 1. Dimensions: order zaroori hai (parent pehle).
            self.step("Teams", importers.import_teams)
            self.step("Players", importers.import_players)
            self.step("Games", importers.import_games)
            self.step("National assist share", importers.import_national_assist_share)

            # 2. Player-season fact tables.
            for model in importers.PLAYER_SEASON_TABLES:
                self.step(model.__name__, importers.import_player_season_table, model, seasons)

            # 3. Possessions (sab se bari, aakhir mein).
            if options["skip_possessions"]:
                self.stdout.write(self.style.WARNING("Possessions skip kiye (--skip-possessions)."))
            else:
                self.step("Possessions", importers.import_possessions, seasons, self.progress)

        except importers.MissingReferenceError as exc:
            # Saaf message, Python ka lamba traceback nahi.
            raise CommandError(f"Import ruk gaya: {exc}") from exc

        self.print_summary()
        self.stdout.write(self.style.SUCCESS(f"Mukammal: {time.monotonic() - started:.1f}s"))

    # -- helpers -----------------------------------------------------------

    def step(self, label, func, *args):
        """Ek importer chalao, waqt aur likhi gayi rows print karo."""
        self.stdout.write(f"{label} ...")
        t0 = time.monotonic()
        written = func(*args)
        details = ", ".join(f"{name}: {count:,}" for name, count in written.items())
        self.stdout.write(f"  {details}  ({time.monotonic() - t0:.1f}s)")

    def progress(self, season, rows_so_far):
        """Possessions import ke dauraan har ~100k rows par line print."""
        if rows_so_far % 100_000 < importers.FETCH_CHUNK:
            self.stdout.write(f"  {season}: {rows_so_far:,} rows")

    def print_summary(self):
        """
        Django tables mein ab kitni rows hain. In numbers ko ASSUMPTIONS.md ke
        verified facts (F-02, F-05, F-06 aur coverage table) se milayein.
        """
        self.stdout.write(self.style.MIGRATE_HEADING("\nSummary (Django tables):"))
        lines = [
            ("Team", Team.objects.count()),
            ("TeamSeason", TeamSeason.objects.count()),
            ("Player", Player.objects.count()),
            ("Game (sab)", Game.objects.count()),
            ("Game (regular season)", Game.objects.regular_season().count()),
            ("NationalAssistShare", NationalAssistShare.objects.count()),
            ("PlayerSeasonCounts", PlayerSeasonCounts.objects.count()),
            ("PlayerSeasonPossessions", PlayerSeasonPossessions.objects.count()),
            ("PlayerSeasonBox", PlayerSeasonBox.objects.count()),
            ("TorvikPlayerSeason", TorvikPlayerSeason.objects.count()),
            ("Possession", Possession.objects.count()),
        ]
        for name, count in lines:
            self.stdout.write(f"  {name:<26}{count:>12,}")