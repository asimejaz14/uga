"""
Level (Step 2) calculate karta hai, spec se muqabla print karta hai, aur
database mein SAVE karta hai.

    python manage.py compute_level --season 2026 --dry-run --player 5174661   # sirf check
    python manage.py compute_level --all                                      # sab seasons save

Har season ki CalculationRun (kind=level) us season ki latest kamyab Role
run par depend karti hai (depends_on). Pehle compute_role chalana zaroori hai.
"""
import time
from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from analytics import loaders
from analytics.choices import RunKind, Tier
from analytics.constants import SPEC_VERSION, constants_snapshot
from analytics.level.pipeline import build_level
from analytics.level.save import save_level_season
from analytics.models import CalculationRun
from basketball.models import Player

# Spec 2026 (V-14, V-15, V-20)
SPEC_2026 = {"replacement_all": -1.75, "guards": -2.16, "wings": -1.63, "bigs": -1.31,
             "bench_players": 556, "d1_teams": 365}
BLUE_CAIN = {"espn_id": 5174661, "epa_total": 100.631, "epa_per40": 4.982, "replacement": -1.634,
             "surplus_per40": 6.616, "war_per40": 0.1587, "war": 3.21}


class Command(BaseCommand):
    help = "Level (Step 2): EPA, replacement, WAR, tier."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, action="append", dest="seasons")
        parser.add_argument("--all", action="store_true")
        parser.add_argument("--dry-run", action="store_true", help="Sirf hisaab aur print, save nahi.")
        parser.add_argument("--player", type=int, help="ESPN player id ka trace.")

    def handle(self, *args, **options):
        if options["all"]:
            seasons = sorted(loaders.seasons_with_counts())
        elif options["seasons"]:
            seasons = options["seasons"]
        else:
            raise CommandError("--season ya --all dein.")

        t0 = time.monotonic()
        try:
            results = build_level(seasons)
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(f"Hisaab: {time.monotonic() - t0:.1f}s")

        for season in seasons:
            data = results[season]
            self.print_season(data)
            if options["player"]:
                self.print_player(data, options["player"])
            if not options["dry_run"]:
                self.save(data)

    # -----------------------------------------------------------------------

    def save(self, data):
        run = CalculationRun(
            kind=RunKind.LEVEL, season=data.season, spec_version=SPEC_VERSION,
            depends_on=data.role_run, constants_snapshot=constants_snapshot(),
        )
        run.full_clean()
        run.save()
        try:
            with transaction.atomic():
                count = save_level_season(run, data)
        except Exception as exc:
            run.mark_failed(exc)
            raise CommandError(f"Season {data.season} fail: {exc}") from exc
        tiers = Counter(str(p.tier) for p in data.players.values() if p.is_qualified)
        run.mark_success({"players": count, "qualified_tiers": dict(tiers),
                          "role_run": data.role_run.pk, "history_complete": data.history_complete})
        self.stdout.write(self.style.SUCCESS(f"  saved: run #{run.pk} · {count:,} players"))

    def print_season(self, data):
        rep, ppw = data.replacement, data.ppw
        spec = SPEC_2026 if data.season == 2026 else {}

        def line(name, ours, key):
            s = f"    {name:<22}{ours:>10.3f}" if isinstance(ours, float) else f"    {name:<22}{ours:>10,}"
            if key in spec:
                s += f"   spec {spec[key]}   diff {ours - spec[key]:+.3f}"
            return s

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nSeason {data.season} · role run #{data.role_run.pk} · history_complete {data.history_complete}"
        ))
        self.stdout.write(line("D1 teams", data.d1_teams, "d1_teams"))
        self.stdout.write(line("bench players", rep.bench_players, "bench_players"))
        self.stdout.write(line("replacement overall", rep.overall, "replacement_all"))
        for family in ("guards", "wings", "bigs"):
            self.stdout.write(line(f"replacement {family}", rep.for_family(family), family))
        self.stdout.write(f"    {'points per win':<22}{ppw.points_per_win:>10.3f}")

        q = [p for p in data.players.values() if p.is_qualified]
        tiers = Counter(p.tier for p in q)
        self.stdout.write(f"  qualified (400+ min, rated, D1): {len(q):,}   "
                          + " · ".join(f"{Tier(t).label} {tiers[t]:,} ({tiers[t] / max(len(q), 1):.0%})" for t in Tier))
        not_rated = sum(1 for p in data.players.values() if not p.is_rated)
        self.stdout.write(f"  not rated (coverage < 0.80 ya points 0): {not_rated:,} / {len(data.players):,}")

        # Pieces ka jama total ke barabar (spec: "reconcile exactly")
        broken = sum(1 for p in data.players.values() if abs(sum(p.pieces.values()) - p.epa_total) > 1e-9)
        self.stdout.write(f"  pieces != total: {broken}  (0 hona chahiye)")

    def print_player(self, data, espn_id):
        player = Player.objects.filter(espn_player_id=espn_id).first()
        p = data.players.get(player.id) if player else None
        if p is None:
            self.stdout.write(self.style.WARNING(f"  Player {espn_id} is season ke Level mein nahi."))
            return
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n  {player.name}, {data.season}"))
        for name, value in p.pieces.items():
            self.stdout.write(f"    {name:<22}{value:>10.3f}")
        spec = BLUE_CAIN if (espn_id == BLUE_CAIN["espn_id"] and data.season == 2026) else {}
        rep = data.replacement.for_family(p.family)
        rows = [
            ("epa_total", p.epa_total), ("minutes", p.minutes), ("coverage", p.coverage),
            ("epa_per40", p.epa_per40), ("family", p.family), ("replacement", rep),
            ("surplus_per40", p.surplus_per40), ("war_per40", p.war_per40), ("war", p.war),
            ("tier", p.tier),
        ]
        for name, value in rows:
            shown = f"{value:>10.4f}" if isinstance(value, float) else f"{str(value):>10}"
            extra = ""
            if name in spec and isinstance(value, float):
                extra = f"   spec {spec[name]}   diff {value - spec[name]:+.4f}"
            self.stdout.write(f"    {name:<22}{shown}{extra}")
