"""
Role steps R4 + R5 (percentiles aur group scores) check karta hai. Database
mein kuch save NAHI karta.

    python manage.py check_role_groups --season 2026
    python manage.py check_role_groups --season 2026 --player 5174661
"""
import statistics
from collections import Counter

from django.core.management.base import BaseCommand, CommandError

from analytics.role.percentiles import top_play_types
from analytics.role.pipeline import build_role_season
from basketball.models import Player


class Command(BaseCommand):
    help = "Role R4+R5: percentiles aur group scores ka khulasa."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, required=True)
        parser.add_argument("--player", type=int, help="ESPN player id ki detail.")

    def handle(self, *args, **options):
        data = build_role_season(options["season"])
        qualified = [p for p in data.qualified if p in data.groups]

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nSeason {data.season} ({data.rules_mode}) · qualified {len(qualified):,}"
        ))

        # Sanity 1: qualified players mein har group score ka average ~0.50 hona chahiye
        # (percentile apni hi population mein barabar phaila hota hai).
        self.stdout.write("  Qualified players mein group score:   mean    min    max")
        for group in data.group_definitions:
            scores = [data.groups[p][group][1] for p in qualified if data.groups[p][group][1] is not None]
            self.stdout.write(f"    {group:<28}{statistics.mean(scores):>8.3f}"
                              f"{min(scores):>7.3f}{max(scores):>7.3f}")

        # Sanity 2: kis group mein qualified players ka sab se ooncha score hai
        # (asal role abhi nahi; sirf andaza ke kaunsa kaam zyada "jeet'ta" hai).
        top_group = Counter()
        for p in qualified:
            scored = [(g, s) for g, (_, s) in data.groups[p].items() if s is not None]
            top_group[max(scored, key=lambda item: item[1])[0]] += 1
        self.stdout.write("\n  Sab se ooncha group (qualified):")
        for group, count in top_group.most_common():
            self.stdout.write(f"    {group:<28}{count:>6,}  ({count / len(qualified):.1%})")

        if options["player"]:
            self.print_player(options["player"], data)

    def print_player(self, espn_id, data):
        player = Player.objects.filter(espn_player_id=espn_id).first()
        if player is None or player.id not in data.groups:
            raise CommandError(f"ESPN id {espn_id} is season ke frame / rates mein nahi.")

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{player.name} ({espn_id}), {data.season}"))
        self.stdout.write(f"  top 4 play types: {top_play_types(data.percentiles[player.id])}")
        self.stdout.write("  group                      raw    score   (members: percentile)")
        ranked = sorted(data.groups[player.id].items(), key=lambda item: item[1][1] or -1, reverse=True)
        for group, (raw, score) in ranked:
            members = ", ".join(
                f"{pt} {'—' if data.percentiles[player.id].get(pt) is None else f'{data.percentiles[player.id][pt]:.2f}'}"
                for pt in data.group_definitions[group]
            )
            raw_s = "  —  " if raw is None else f"{raw:.3f}"
            score_s = "  —  " if score is None else f"{score:.3f}"
            self.stdout.write(f"    {group:<22}{raw_s:>7}{score_s:>8}   ({members})")
