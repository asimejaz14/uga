"""
Role steps R2 + R3 (play-type rates) chala kar check karta hai. Database
mein kuch save NAHI karta.

    python manage.py check_role_rates --season 2026
    python manage.py check_role_rates --season 2026 --player 5174661    # Blue Cain ki detail
"""
import statistics

from django.core.management.base import BaseCommand, CommandError

from analytics import loaders
from analytics.constants import GROUP_PLAY_TYPES
from analytics.role import pooling
from analytics.role.play_types import player_rates
from basketball.models import Player

SPEC_QUALIFIED_2026 = 2284


class Command(BaseCommand):
    help = "Role R2+R3: play-type rates ka khulasa (qualified players ke medians)."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, required=True)
        parser.add_argument("--player", type=int, help="ESPN player id: us player ki detail bhi print karo.")

    def handle(self, *args, **options):
        season = options["season"]
        seasons = [season, season - 1, season - 2]

        # --- Data ---
        frame = loaders.role_frame(season)
        mode = loaders.rules_mode_for_season(season)
        national_share = loaders.national_assist_shares(season)
        rows = loaders.role_rows_lookup(frame, seasons)
        off_lookup = {key: row["off_poss"] for key, row in rows.items()}
        pool_results = pooling.decide_pooling_for_season(
            season, frame, off_lookup, loaders.seasons_in_data()
        )
        qualified = loaders.qualified_player_ids(season, frame)

        # --- R2 + R3 har player ke liye ---
        rates = {}
        for player_id, result in pool_results.items():
            if result.status == pooling.NO_DATA:
                continue
            rows_by_season = {s: rows[(player_id, s)] for s in seasons if (player_id, s) in rows}
            rates[player_id] = player_rates(rows_by_season, result.weights, season, national_share, mode)

        # --- Khulasa ---
        self.stdout.write(self.style.MIGRATE_HEADING(f"\nSeason {season}  (rules mode: {mode})"))
        line = f"  qualified: {len(qualified):,}"
        if season == 2026:
            line += f"   spec {SPEC_QUALIFIED_2026:,}   diff {len(qualified) - SPEC_QUALIFIED_2026:+,}"
        self.stdout.write(line)
        self.stdout.write(f"  rates bane: {len(rates):,} players\n")

        self.stdout.write("  Qualified players mein (per 100):     median      max    blank")
        for group, play_types in GROUP_PLAY_TYPES[mode].items():
            self.stdout.write(f"  [{group}]")
            for play_type in play_types:
                values = [rates[p][play_type] for p in qualified if p in rates]
                present = [v for v in values if v is not None]
                blank = len(values) - len(present)
                median = statistics.median(present) if present else float("nan")
                maximum = max(present) if present else float("nan")
                self.stdout.write(f"    {play_type:<22}{median:>14.2f}{maximum:>9.2f}{blank:>9,}")

        # --- Ek player ki detail ---
        if options["player"]:
            self.print_player(options["player"], season, pool_results, rates, rows, qualified, mode)

    def print_player(self, espn_id, season, pool_results, rates, rows, qualified, mode):
        try:
            player = Player.objects.get(espn_player_id=espn_id)
        except Player.DoesNotExist:
            raise CommandError(f"ESPN id {espn_id} ka player nahi mila.")
        if player.id not in pool_results:
            raise CommandError(f"{player.name} is season ke frame mein nahi.")

        result = pool_results[player.id]
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{player.name} ({espn_id}), {season}"))
        self.stdout.write(f"  status {result.status} · weights {result.weights} · "
                          f"pooled off_poss {result.pooled_off_poss:,.1f} · qualified {player.id in qualified}")
        current = rows.get((player.id, season), {})
        self.stdout.write(f"  is season: off_poss {current.get('off_poss')} · "
                          f"def_poss {current.get('def_poss')} · tagged_off_poss {current.get('tagged_off_poss')}")
        for group, play_types in GROUP_PLAY_TYPES[mode].items():
            parts = []
            for play_type in play_types:
                value = rates.get(player.id, {}).get(play_type)
                parts.append(f"{play_type} {'—' if value is None else f'{value:.2f}'}")
            self.stdout.write(f"  [{group}] " + " · ".join(parts))
