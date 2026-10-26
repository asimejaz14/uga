"""
Role calculate kar ke database mein SAVE karta hai (Step 1 ka aakhri hissa).

    python manage.py compute_role --season 2026
    python manage.py compute_role --season 2024 --season 2025 --season 2026
    python manage.py compute_role --all          # database ke saare seasons

Har season ki apni CalculationRun banti hai:
    running -> (placements + group scores likhe) -> success
Ghalti ho to run "failed" ho jati hai aur us ke adhoore results wapas
(transaction). API hamesha latest SUCCESS run parhti hai (D-06), is liye
fail run kabhi nazar nahi aati.
"""
import time
from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from analytics import loaders
from analytics.choices import RunKind
from analytics.constants import SPEC_VERSION, constants_snapshot
from analytics.models import CalculationRun
from analytics.role.pipeline import build_full_role_season
from analytics.role.save import save_role_season


class Command(BaseCommand):
    help = "Role (Step 1) calculate kar ke RolePlacement aur GroupScore mein save karta hai."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, action="append", dest="seasons")
        parser.add_argument("--all", action="store_true", help="Database ke saare seasons.")

    def handle(self, *args, **options):
        if options["all"]:
            seasons = sorted(loaders.seasons_in_data())
        elif options["seasons"]:
            seasons = options["seasons"]
        else:
            raise CommandError("--season ya --all dein.")

        for season in seasons:
            self.compute(season)

    def compute(self, season):
        t0 = time.monotonic()
        self.stdout.write(f"Season {season}: Role ...")

        # 1. Run banao (status = running)
        run = CalculationRun(
            kind=RunKind.ROLE,
            season=season,
            spec_version=SPEC_VERSION,
            constants_snapshot=constants_snapshot(),
        )
        run.full_clean()
        run.save()

        try:
            # 2. Hisaab (database sirf parhta hai)
            data = build_full_role_season(season)

            # 3. Likhna: sab ya kuch nahi
            with transaction.atomic():
                summary = save_role_season(run, data)

        except Exception as exc:
            run.mark_failed(exc)
            raise CommandError(f"Season {season} fail: {exc}") from exc

        # 4. Kamyab: ab API isay dekhegi
        run.mark_success(summary)

        roles = Counter(summary["qualified_roles"])
        self.stdout.write(self.style.SUCCESS(
            f"  run #{run.pk} success · {summary['frame']:,} placements · "
            f"{summary['group_score_rows']:,} group scores · {time.monotonic() - t0:.1f}s"
        ))
        self.stdout.write(f"  qualified roles: " + ", ".join(f"{r} {n}" for r, n in roles.most_common()))
