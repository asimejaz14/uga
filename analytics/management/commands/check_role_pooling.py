"""
Role step R1 (pooling) chala kar natija print karta hai. Database mein kuch
save NAHI karta; sirf validation ke liye.

    python manage.py check_role_pooling --season 2026
    python manage.py check_role_pooling --season 2024 --season 2025 --season 2026
"""
from collections import Counter

from django.core.management.base import BaseCommand

from analytics import loaders
from analytics.role import pooling

# Spec ke 2026 numbers (ASSUMPTIONS.md V-02..V-05).
SPEC_2026 = {"frame": 4978, "normal": 3350, "pooled": 319, "fallback": 1309}


class Command(BaseCommand):
    help = "Role R1: frame, pooling aur confidence ke counts."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, action="append", dest="seasons", required=True)

    def handle(self, *args, **options):
        available = loaders.seasons_in_data()
        for season in options["seasons"]:
            self.check_season(season, available)

    def check_season(self, season, available):
        # 1. Kin ko place karna hai
        frame = loaders.role_frame(season)

        # 2. Un ke teen seasons ke possessions
        lookup = loaders.off_possessions_lookup(frame, [season, season - 1, season - 2])

        # 3. Har player ka faisla (pure function)
        results = pooling.decide_pooling_for_season(season, frame, lookup, available)

        # 4. Ginti
        by_status = Counter(r.status for r in results.values())
        grouped = {
            "frame": len(results),
            "normal": by_status[pooling.ESTABLISHED],
            "pooled": by_status[pooling.POOLED] + by_status[pooling.POOLED_THREE],
            "fallback": by_status[pooling.FALLBACK] + by_status[pooling.NO_DATA],
        }
        incomplete = sum(1 for r in results.values() if not r.history_complete)
        no_current_row = sum(1 for p in frame if (p, season) not in lookup)

        # 5. Print
        self.stdout.write(self.style.MIGRATE_HEADING(f"\nSeason {season}"))
        targets = SPEC_2026 if season == 2026 else {}
        for name, value in grouped.items():
            line = f"  {name:<10}{value:>8,}"
            if name in targets:
                diff = value - targets[name]
                line += f"   spec {targets[name]:>6,}   diff {diff:+,}"
            self.stdout.write(line)

        self.stdout.write("  detail:")
        for status in (pooling.ESTABLISHED, pooling.POOLED, pooling.POOLED_THREE,
                       pooling.FALLBACK, pooling.NO_DATA):
            self.stdout.write(f"    {status:<14}{by_status[status]:>8,}")
        self.stdout.write(f"  history_complete = False: {incomplete:,}")
        self.stdout.write(f"  frame mein, lekin is season possessions ki row nahi: {no_current_row:,}")
