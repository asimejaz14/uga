"""
Role step R6 (teammate shares) check karta hai. Database mein kuch save NAHI karta.

    python manage.py check_role_shares --season 2026
    python manage.py check_role_shares --season 2026 --player 5174661
"""
import time

from django.core.management.base import BaseCommand, CommandError

from analytics.role.pipeline import build_role_season
from basketball.models import Player


class Command(BaseCommand):
    help = "Role R6: lead, lead2, inside, inside2, front ka khulasa."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, required=True)
        parser.add_argument("--player", type=int, help="ESPN player id ki detail.")

    def handle(self, *args, **options):
        t0 = time.monotonic()
        data = build_role_season(options["season"], with_shares=True)
        elapsed = time.monotonic() - t0
        totals = data.share_totals
        shares = data.shares

        self.stdout.write(self.style.MIGRATE_HEADING(f"\nSeason {data.season}  ({elapsed:.1f}s)"))
        self.stdout.write(f"  offensive possessions (gine gaye):     {totals['possessions']:>10,}")
        valid_pct = totals["valid_possessions"] / max(totals["possessions"], 1)
        self.stdout.write(f"  jin mein 4+ players ka read:           {totals['valid_possessions']:>10,}  ({valid_pct:.1%})")

        # Check 1: har valid possession mein kam az kam ek "rank 1" passer.
        # Ties ki wajah se thora 1.00 se upar ho sakta hai, neeche kabhi nahi.
        ratio = totals["lead_firsts"] / max(totals["valid_possessions"], 1)
        self.stdout.write(f"  lead rank-1 per valid possession:      {ratio:>10.3f}   (1.000 ya thora upar)")

        # Check 2: lead2 >= lead har player ke liye
        broken = [p for p, s in shares.items() if s.lead is not None and s.lead2 < s.lead]
        self.stdout.write(f"  lead2 < lead wale players:             {len(broken):>10,}   (0 hona chahiye)")

        # Qualified players ki tasveer
        q = [shares[p] for p in data.qualified if p in shares]
        with_shares = [s for s in q if s.lead is not None]
        self.stdout.write(f"\n  qualified: {len(data.qualified):,} · shares mile: {len(with_shares):,} · "
                          f"NULL (200 se kam): {len(q) - len(with_shares):,} · koi valid possession nahi: "
                          f"{len(data.qualified) - len(q):,}")
        for name in ("lead", "inside", "inside2", "front"):
            n = sum(1 for s in with_shares if getattr(s, name) is not None and getattr(s, name) >= 0.5)
            self.stdout.write(f"    {name:<8} >= 50%: {n:>6,}  ({n / max(len(with_shares), 1):.1%})")

        if options["player"]:
            player = Player.objects.filter(espn_player_id=options["player"]).first()
            if player is None or player.id not in shares:
                raise CommandError("Player ke shares nahi mile (frame / read nahi?).")
            s = shares[player.id]
            fmt = lambda v: "—" if v is None else f"{v:.1%}"
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n{player.name}: height {data.heights.get(player.id)}"))
            self.stdout.write(f"  valid_poss {s.valid_poss:,} · lead {fmt(s.lead)} · lead2 {fmt(s.lead2)} · "
                              f"inside {fmt(s.inside)} · inside2 {fmt(s.inside2)} · front {fmt(s.front)}")
