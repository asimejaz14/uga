"""
Role steps R7 + R8 (+ R9): poora Role faisla, spec ke numbers se muqabla.
Database mein kuch save NAHI karta.

    python manage.py check_role_placement --season 2026
    python manage.py check_role_placement --season 2026 --player 5174661
"""
import time
from collections import Counter

from django.core.management.base import BaseCommand, CommandError

from analytics.choices import DecidedBy, Role
from analytics.role.pipeline import build_full_role_season, player_facts
from basketball.models import Player

# Spec 2026: qualified players mein role shares (V-06) aur "decided by" (V-07, read players)
SPEC_ROLE_SHARES = {
    Role.FLOOR_GENERAL: 15.8, Role.COMBO_GUARD: 12.9, Role.GUARD: 10.1,
    Role.THREE_PT_SPECIALIST: 11.8, Role.THREE_AND_D_WING: 7.5, Role.WING: 5.5,
    Role.TRADITIONAL_FORWARD: 18.0, Role.UGA_BIG: 10.9, Role.TRADITIONAL_BIG: 7.5,
}
SPEC_DECIDED_BY = {
    DecidedBy.CLEAR_TOP_GROUP: 2310, DecidedBy.TB_CREATOR: 280, DecidedBy.TB_INTERIOR: 262,
    DecidedBy.TB_LENGTH: 152, DecidedBy.TB_LARGER_SAMPLE: 175, DecidedBy.TB_HIGHER_VOLUME: 490,
}


class Command(BaseCommand):
    help = "Role R7+R8: roles ke shares aur 'decided by' ka spec se muqabla."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, required=True)
        parser.add_argument("--player", type=int, help="ESPN player id: poora trace.")

    def handle(self, *args, **options):
        t0 = time.monotonic()
        data = build_full_role_season(options["season"])
        is_2026 = data.season == 2026
        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nSeason {data.season} ({data.rules_mode})  ·  {time.monotonic() - t0:.1f}s"
        ))

        # --- V-06: qualified players mein role shares ---
        qualified = [data.decisions[p] for p in data.qualified if data.decisions.get(p)]
        roles = Counter(d.primary for d in qualified)
        self.stdout.write(f"\n  Role shares (qualified {len(qualified):,}):      hamara    spec")
        for role in Role:
            ours = roles[role] / max(len(qualified), 1) * 100
            spec = f"{SPEC_ROLE_SHARES[role]:>6.1f}%" if is_2026 else ""
            self.stdout.write(f"    {role.label:<26}{roles[role]:>6,}  {ours:>5.1f}%  {spec}")

        # --- V-07: read players mein "decided by" ---
        read = [d for p, d in data.decisions.items() if d and data.pooling[p].has_read]
        decided = Counter(d.decided_by for d in read)
        self.stdout.write(f"\n  Decided by (read players {len(read):,}):        hamara    spec")
        for name, spec in SPEC_DECIDED_BY.items():
            spec_s = f"{spec:>6,}" if is_2026 else ""
            self.stdout.write(f"    {DecidedBy(name).label:<38}{decided[name]:>6,}  {spec_s}")
        close = sum(1 for d in read if d.decided_by != DecidedBy.CLEAR_TOP_GROUP)
        self.stdout.write(f"    close calls: {close / max(len(read), 1):.1%}  (spec: 38%)")

        # --- Baaqi ---
        fallback = sum(1 for p, d in data.decisions.items() if d and data.pooling[p].fallback)
        no_role = sum(1 for d in data.decisions.values() if d is None)
        self.stdout.write(f"\n  fallback placeholder se: {fallback:,} · role nahi (no data): {no_role:,}")

        if options["player"]:
            self.print_trace(options["player"], data)

    def print_trace(self, espn_id, data):
        player = Player.objects.filter(espn_player_id=espn_id).first()
        if player is None or player.id not in data.decisions:
            raise CommandError("Player is season ke frame mein nahi.")
        d = data.decisions[player.id]
        f = player_facts(data, player.id)
        pct = lambda v: "—" if v is None else f"{v:.1%}"

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{player.name} ({espn_id}), {data.season}"))
        self.stdout.write(f"  height {f.height} · lead {pct(f.lead)} · inside {pct(f.inside)} · "
                          f"inside2 {pct(f.inside2)} · front {pct(f.front)}")
        self.stdout.write(f"  usage {f.usage} (median {data.usage_median}) · 3PA share {f.three_pa_share}")
        if d is None:
            self.stdout.write("  Role nahi (no data).")
            return
        self.stdout.write("  Proposals (score ke hisaab se):")
        for p in sorted(d.proposals, key=lambda p: p.score, reverse=True):
            dropped = "  [guardrail ne hataya]" if p.dropped_by_guardrail else ""
            three = (data.three_season.get(player.id) or {}).get(p.group)
            three_s = "—" if three is None else f"{three:.3f}"
            self.stdout.write(f"    {p.group:<18}{p.score:.3f}  -> {Role(p.role).label:<22}"
                              f"3-season {three_s}{dropped}")
        self.stdout.write(self.style.SUCCESS(
            f"  PRIMARY {Role(d.primary).label} · secondary "
            f"{Role(d.secondary).label if d.secondary else '—'} · family {d.family} · "
            f"group {d.winning_group} · decided by {DecidedBy(d.decided_by).label}"
        ))
