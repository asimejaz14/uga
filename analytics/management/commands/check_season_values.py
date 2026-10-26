"""
Season ke league values aur points per win nikal kar print karta hai, aur
2026 ke liye spec ke numbers se muqabla karta hai. Database mein kuch save
NAHI karta; ye validation ke liye hai (Phase 4a).

    python manage.py check_season_values --season 2026
    python manage.py check_season_values --season 2024 --season 2025 --season 2026
"""
from django.core.management.base import BaseCommand

from analytics import loaders
from analytics.level.league import fit_points_per_win, league_values

# Spec ke 2026 numbers (ASSUMPTIONS.md V-10..V-17) aur kitna farq qabool hai.
SPEC_TARGETS = {
    2026: {
        "xpts_rim": (1.3100, 0.001),
        "xpts_mid": (0.9548, 0.001),
        "xpts_three": (1.2139, 0.001),
        "league_ft_pct": (0.7223, 0.001),
        "ppw_teams": (365, 0),
        "ppw_intercept": (14.75, 0.005),
        "ppw_slope": (0.02399, 0.000005),
        "ppw_r": (0.933, 0.0005),
        "points_per_win": (41.69, 0.005),
    },
}


class Command(BaseCommand):
    help = "League values (xPTS, FT%, jumper share) aur points per win check karta hai."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, action="append", dest="seasons", required=True)

    def handle(self, *args, **options):
        for season in options["seasons"]:
            self.check_season(season)

    def check_season(self, season):
        values = league_values(loaders.league_shot_totals(season), loaders.national_assist_shares(season))
        fit = fit_points_per_win(loaders.d1_team_records(season))

        ours = {
            "xpts_rim": values.xpts["rim"],
            "xpts_mid": values.xpts["mid"],
            "xpts_three": values.xpts["three"],
            "league_ft_pct": values.league_ft_pct,
            "ast_share_jumper": values.ast_share_jumper,
            "ppw_teams": fit.teams,
            "ppw_intercept": fit.intercept,
            "ppw_slope": fit.slope,
            "ppw_r": fit.r,
            "points_per_win": fit.points_per_win,
        }
        targets = SPEC_TARGETS.get(season, {})

        self.stdout.write(self.style.MIGRATE_HEADING(f"\nSeason {season}"))
        for name, value in ours.items():
            shown = f"{value:>12}" if isinstance(value, int) else f"{value:>12.6f}"
            line = f"  {name:<18}{shown}"
            if name in targets:
                spec, tolerance = targets[name]
                diff = value - spec
                ok = abs(diff) <= tolerance
                status = self.style.SUCCESS("OK") if ok else self.style.ERROR("FARQ")
                line += f"   spec {spec:<10} diff {diff:+.6f}  {status}"
            self.stdout.write(line)
