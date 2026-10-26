"""
Compare what the pipeline wrote against the answer keys from the dummy-data generator.

    python manage.py seed_role_dummy --flush --check-dir checks   # 1. seed + write answer keys
    python manage.py run_role                                     # 2. run the pipeline
    python manage.py verify_role_steps --check-dir checks         # 3. compare

Checks against answer keys (Steps 1-2, saved in the DB):
  possessions   PlayerSeasonPossessions  vs checks/expected_possessions.csv   (must match exactly)
  assist_share  NationalAssistShare      vs checks/expected_assist_share.csv  (within 0.0001)

Checks on the in-memory steps (3-4), when you also pass --dump-dir:
    python manage.py run_role --dump-dir dumps
    python manage.py verify_role_steps --check-dir checks --dump-dir dumps

  pooling     qualified flag and pooled off_poss recomputed row by row from the DB,
              with a deliberately simple loop (a second, independent implementation)
  play_types  percentiles inside 0-1; 16 play types in coarse seasons, 21 in full;
              rate_assists = pooled assists / pooled off_poss x 100
  shares      PlayerOnfloorShares recomputed with a plain possession-by-possession loop
  groups      raw group score = mean of the top two percentiles, recomputed with sorted()
  placement   rules the output must always obey (family matches primary, secondary differs,
              guardrails respected) + a report against DummyTruth (how often the true
              archetype was found) + role shares vs the spec's 3%-30% check
  sanity      a table of mean percentile by TRUE archetype (DummyTruth) for signature
              play types. A Floor General should top assists, a UGA Big blocks, etc.
              This is a WARN, not a FAIL: dummy data is random, so one miss is possible,
              but many misses means the play types are wired to the wrong columns.

Exit code is 1 if anything fails, so it can run in CI.
"""
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from ...models import (
    DummyTruth, Game, NationalAssistShare, PlayerOnfloorShares, PlayerSeasonCounts,
    PlayerSeasonPossessions, Possession, RolePlacement, TorvikPlayerSeason,
)
from ...role_pipeline.groups import groups_for
from ...role_pipeline.rules import FAMILY

TOLERANCE = 0.0001   # NationalAssistShare stores 4 decimal places

# (archetype, play type) pairs where the archetype should be among the top 2 archetypes
SIGNATURES = [
    ("Floor General", "assists"),
    ("Combo Guard", "own_threes"),
    ("Guard", "steals"),
    ("3pt Specialist", "cs_threes"),
    ("Wing", "ft_trips"),
    ("Traditional Forward", "drb"),
    ("UGA Big", "blocks"),
    ("Traditional Big", "drb"),
]


class Command(BaseCommand):
    help = "Verify Role pipeline outputs against the dummy-data answer keys."

    def add_arguments(self, parser):
        parser.add_argument("--check-dir", required=True, metavar="DIR")
        parser.add_argument("--dump-dir", metavar="DIR",
                            help="also check Steps 3-4 using the CSVs from run_role --dump-dir")
        parser.add_argument("--show", type=int, default=10,
                            help="how many mismatching rows to print (default 10)")

    def handle(self, *args, **opts):
        d = Path(opts["check_dir"])
        self.show = opts["show"]
        ok = self.check_possessions(d / "expected_possessions.csv")
        ok &= self.check_assist_share(d / "expected_assist_share.csv")
        if opts["dump_dir"]:
            dump = Path(opts["dump_dir"])
            seasons = sorted(int(p.stem.split("_")[-1]) for p in dump.glob("pooled_2*.csv"))
            if not seasons:
                ok &= self._fail("dumps", f"no pooled_<season>.csv in {dump}")
            for s in seasons:
                ok &= self.check_pooling(dump, s)
                ok &= self.check_play_types(dump, s)
                if (dump / f"shares_{s}.csv").exists():
                    ok &= self.check_shares(dump, s)
                if (dump / f"group_scores_{s}.csv").exists():
                    ok &= self.check_groups(dump, s)
                    ok &= self.check_placement(s)
            if seasons:
                self.sanity_by_archetype(dump, seasons[-1])
                self.placement_report(seasons)
        if not ok:
            raise CommandError("verification failed")
        self.stdout.write(self.style.SUCCESS("All checks passed."))

    # ------------------------------------------------------------------------

    def check_possessions(self, path):
        exp = pd.read_csv(path)
        got = pd.DataFrame(PlayerSeasonPossessions.objects.values(
            "player_id", "season", "off_poss", "def_poss", "tagged_off_poss"))
        if got.empty:
            return self._fail("possessions", "PlayerSeasonPossessions is empty — run run_role first")

        # Outer join on the key so we also catch rows that exist on only one side.
        m = exp.merge(got, on=["player_id", "season"], how="outer",
                      suffixes=("_exp", "_got"), indicator=True)
        only_exp = m[m["_merge"] == "left_only"]
        only_got = m[m["_merge"] == "right_only"]
        both = m[m["_merge"] == "both"]

        bad = pd.Series(False, index=both.index)
        for col in ["off_poss", "def_poss", "tagged_off_poss"]:
            e = both[f"{col}_exp"].astype("Float64")
            g = both[f"{col}_got"].astype("Float64")
            # equal, or both blank (tagged_off_poss is blank before 2026)
            same = (e == g).fillna(False) | (e.isna() & g.isna())
            bad |= ~same

        problems = len(only_exp) + len(only_got) + int(bad.sum())
        self.stdout.write(f"possessions:  {len(exp)} expected, {len(got)} in DB, "
                          f"{len(only_exp)} missing, {len(only_got)} extra, "
                          f"{int(bad.sum())} with different numbers")
        if problems:
            cols = ["player_id", "season"] + [f"{c}_{s}" for c in
                    ["off_poss", "def_poss", "tagged_off_poss"] for s in ("exp", "got")]
            self.stdout.write(pd.concat([only_exp, only_got, both[bad]])[cols]
                              .head(self.show).to_string(index=False))
            return self._fail("possessions")
        return self._pass("possessions")

    def check_assist_share(self, path):
        exp = pd.read_csv(path)
        got = pd.DataFrame(NationalAssistShare.objects.values("season", "zone", "ast_share"))
        if got.empty:
            return self._fail("assist_share", "NationalAssistShare is empty — run run_role first")
        got["ast_share"] = got["ast_share"].astype(float)

        m = exp.merge(got, on=["season", "zone"], how="outer", suffixes=("_exp", "_got"))
        m["diff"] = (m["ast_share_exp"] - m["ast_share_got"]).abs()
        bad = m[m["diff"].isna() | (m["diff"] > TOLERANCE)]
        self.stdout.write(f"assist_share: {len(exp)} expected, {len(got)} in DB, "
                          f"{len(bad)} off by more than {TOLERANCE}")
        if len(bad):
            self.stdout.write(bad.head(self.show).to_string(index=False))
            return self._fail("assist_share")
        return self._pass("assist_share")

    # ---- Step 3 ------------------------------------------------------------

    def check_pooling(self, dump, season):
        """Recompute pooled off_poss and qualified with a plain loop and compare."""
        got = pd.read_csv(dump / f"pooled_{season}.csv").set_index("player_id")
        poss = {(r["player_id"], r["season"]): r["off_poss"] for r in
                PlayerSeasonPossessions.objects.filter(season__in=[season - 2, season - 1, season])
                .values("player_id", "season", "off_poss")}
        min_pct = {r["player_id"]: float(r["min_pct"]) for r in
                   TorvikPlayerSeason.objects.filter(season=season).values("player_id", "min_pct")}

        bad = []
        for pid, row in got.iterrows():
            this = poss.get((pid, season), 0)
            last = poss.get((pid, season - 1), 0)
            before = poss.get((pid, season - 2), 0)
            if this >= 300:                      # established
                expected = this + 0.5 * last
            else:                                # low-minute
                expected = this + last
                if expected < 300:
                    expected += before
            qualified = min_pct.get(pid, -1) >= 40 and this >= 300
            if abs(row["off_poss"] - expected) > 1e-6 or bool(row["qualified"]) != qualified:
                bad.append((pid, row["off_poss"], expected, row["qualified"], qualified))

        self.stdout.write(f"pooling {season}: {len(got)} players, {len(bad)} differ")
        if bad:
            self.stdout.write(pd.DataFrame(bad, columns=["player_id", "off_poss_got", "off_poss_exp",
                              "qualified_got", "qualified_exp"]).head(self.show).to_string(index=False))
            return self._fail(f"pooling {season}")
        return self._pass(f"pooling {season}")

    # ---- Step 4 ------------------------------------------------------------

    def check_play_types(self, dump, season):
        pt = pd.read_csv(dump / f"play_types_{season}.csv")
        pooled = pd.read_csv(dump / f"pooled_{season}.csv").set_index("player_id")
        problems = []

        pctl = pt.filter(like="pctl_")
        if ((pctl < 0) | (pctl > 1)).any().any():
            problems.append("a percentile is outside 0-1")

        mode = pt["mode"].iloc[0]
        expected_n = 21 if mode == "full" else 16
        if pctl.shape[1] != expected_n:
            problems.append(f"{pctl.shape[1]} play types, expected {expected_n} for {mode} rules")

        p = pooled.loc[pt["player_id"]]
        manual = (p["assists"] / p["off_poss"].where(p["off_poss"] > 0) * 100).to_numpy()
        diff = (pt["rate_assists"].to_numpy() - manual)
        if (abs(diff[~pd.isna(diff)]) > 1e-4).any():
            problems.append("rate_assists != pooled assists / pooled off_poss x 100")

        self.stdout.write(f"play_types {season}: {mode} rules, {pctl.shape[1]} play types, "
                          f"{len(problems)} problems")
        for msg in problems:
            self.stdout.write(f"    - {msg}")
        return self._fail(f"play_types {season}") if problems else self._pass(f"play_types {season}")

    # ---- Step 5 ------------------------------------------------------------

    def check_shares(self, dump, season):
        """Recompute every share with a slow, obvious loop and compare with the DB.

        This loop is written differently on purpose (no numpy tricks), so if both
        agree, the fast version in shares.py is very likely right.
        """
        pt = pd.read_csv(dump / f"play_types_{season}.csv").set_index("player_id")
        pooled = pd.read_csv(dump / f"pooled_{season}.csv").set_index("player_id")
        read = pooled["read"].to_dict()
        height = pooled["height_in"].to_dict()
        passing = pt["rate_assists"].to_dict()
        interior = (pt["rate_orb"] + pt["rate_blocks"] + pt["rate_putbacks"]).to_dict()

        ok_games = set(Game.objects.filter(season=season, season_type=2, tournament_id__isnull=True)
                       .values_list("game_id", flat=True))
        tally = {}   # player -> counters
        rows = Possession.objects.filter(season=season, garbage_time=False).values_list(
            "game_id", "off_p1", "off_p2", "off_p3", "off_p4", "off_p5")
        for game_id, *five in rows:
            if game_id not in ok_games or None in five or len(set(five)) != 5:
                continue
            if sum(bool(read.get(p, False)) for p in five) < 4:
                continue                                   # fewer than 4 reads
            all_heights = all(not pd.isna(height.get(p)) for p in five)
            for me in five:
                t = tally.setdefault(me, dict(n=0, lead=0, lead2=0, inside=0, inside2=0,
                                              fn=0, front=0))

                def rank(values):
                    mine = values.get(me) if read.get(me) else None
                    mine = float("-inf") if mine is None or pd.isna(mine) else mine
                    others = []
                    for o in five:
                        if o == me:
                            continue
                        v = values.get(o) if read.get(o) else None
                        others.append(float("-inf") if v is None or pd.isna(v) else v)
                    return 1 + sum(o > mine for o in others)

                t["n"] += 1
                r = rank(passing)
                t["lead"] += r == 1
                t["lead2"] += r <= 2
                r = rank(interior)
                t["inside"] += r == 1
                t["inside2"] += r <= 2
                if all_heights:
                    taller = sum(height[o] > height[me] for o in five if o != me)
                    t["fn"] += 1
                    t["front"] += taller < 2

        db = {r["player_id"]: r for r in PlayerOnfloorShares.objects.filter(season=season).values()}
        bad = []
        for pid, t in tally.items():
            exp = {k: (t[k] / t["n"] if t["n"] >= 200 else None)
                   for k in ("lead", "lead2", "inside", "inside2")}
            exp["front"] = t["front"] / t["fn"] if t["fn"] >= 200 else None
            got = db.get(pid)
            if got is None or got["valid_poss"] != t["n"]:
                bad.append((pid, "valid_poss", t["n"], None if got is None else got["valid_poss"]))
                continue
            for k, e in exp.items():
                g = got[k]
                if (e is None) != (g is None) or (e is not None and abs(float(g) - e) > 6e-5):
                    bad.append((pid, k, e, g))

        self.stdout.write(f"shares {season}: {len(tally)} players recomputed by loop, {len(bad)} differ")
        if bad:
            self.stdout.write(pd.DataFrame(bad, columns=["player_id", "field", "loop", "db"])
                              .head(self.show).to_string(index=False))
            return self._fail(f"shares {season}")
        return self._pass(f"shares {season}")

    # ---- Step 6 ------------------------------------------------------------

    def check_groups(self, dump, season):
        """raw_<group> must equal the mean of the two highest member percentiles."""
        pt = pd.read_csv(dump / f"play_types_{season}.csv").set_index("player_id")
        gs = pd.read_csv(dump / f"group_scores_{season}.csv").set_index("player_id")
        mode = pt["mode"].iloc[0]
        bad = 0
        for pid in gs.index:
            for g, members in groups_for(mode).items():
                vals = [pt.at[pid, f"pctl_{m}"] for m in members]
                vals = sorted([v for v in vals if not pd.isna(v)], reverse=True)[:2]
                exp = sum(vals) / len(vals) if vals else None
                got = gs.at[pid, f"raw_{g}"]
                if (exp is None) != pd.isna(got) or (exp is not None and abs(exp - got) > 1e-6):
                    bad += 1
        self.stdout.write(f"groups {season}: {len(gs)} players x 7 groups, {bad} raw scores differ")
        return self._fail(f"groups {season}") if bad else self._pass(f"groups {season}")

    # ---- Steps 7-8 ---------------------------------------------------------

    def check_placement(self, season):
        """Things that must be true for EVERY placement, whatever the data."""
        rp = pd.DataFrame(RolePlacement.objects.filter(season=season).values(
            "player_id", "primary_role", "secondary_role", "family"))
        tv = pd.DataFrame(TorvikPlayerSeason.objects.filter(season=season).values(
            "player_id", "height_in"))
        if rp.empty:
            return self._fail(f"placement {season}", "RolePlacement is empty")
        rp = rp.merge(tv, on="player_id", how="left")
        h = rp["height_in"].astype(float)
        problems = {
            "family does not match primary role": (rp["family"] != rp["primary_role"].map(FAMILY)).sum(),
            "secondary equals primary": (rp["secondary_role"] == rp["primary_role"]).sum(),
            "big role under 6'5\"": (rp["primary_role"].isin(["UGA Big", "Traditional Big"]) & (h < 77)).sum(),
            "guard role over 6'8\"": (rp["primary_role"].isin(
                ["Floor General", "Combo Guard", "Guard"]) & (h > 80)).sum(),
        }
        bad = {k: int(v) for k, v in problems.items() if v}
        self.stdout.write(f"placement {season}: {len(rp)} placements, {sum(bad.values())} rule breaks")
        for k, v in bad.items():
            self.stdout.write(f"    - {k}: {v}")
        return self._fail(f"placement {season}") if bad else self._pass(f"placement {season}")

    def placement_report(self, seasons):
        """Not pass/fail: how the placements look against the truth and the spec's checks."""
        rp = pd.DataFrame(RolePlacement.objects.filter(season__in=seasons).values(
            "player_id", "season", "primary_role", "secondary_role", "family", "fallback",
            "decided_by"))
        truth = pd.DataFrame(DummyTruth.objects.filter(season__in=seasons).values(
            "player_id", "season", "archetype"))
        self.stdout.write("\nplacement report (players with a read)")
        r = rp[~rp["fallback"]]
        self.stdout.write("  decided by: " + ", ".join(
            f"{k} {v}" for k, v in r["decided_by"].value_counts().items()))
        shares = r["primary_role"].value_counts(normalize=True)
        self.stdout.write(f"  smallest / largest role share: {shares.min():.1%} / {shares.max():.1%}"
                          "   (spec target: 3% to 30%)")
        if not truth.empty:
            m = r.merge(truth, on=["player_id", "season"])
            role = (m["primary_role"] == m["archetype"]).mean()
            fam = (m["family"] == m["archetype"].map(FAMILY)).mean()
            either = ((m["primary_role"] == m["archetype"]) |
                      (m["secondary_role"] == m["archetype"])).mean()
            self.stdout.write(f"  vs DummyTruth: role {role:.0%}, family {fam:.0%}, "
                              f"role as primary or secondary {either:.0%}")

    def sanity_by_archetype(self, dump, season):
        """Mean percentile per TRUE archetype; qualified players only."""
        pt = pd.read_csv(dump / f"play_types_{season}.csv")
        truth = pd.DataFrame(DummyTruth.objects.filter(season=season).values("player_id", "archetype"))
        if truth.empty:
            self.stdout.write("sanity: no DummyTruth rows (real data?) - skipped")
            return
        df = pt[pt["qualified"]].merge(truth, on="player_id")
        cols = sorted({f"pctl_{c}" for _, c in SIGNATURES})
        table = df.groupby("archetype")[cols].mean().round(2)
        table.columns = [c.removeprefix("pctl_") for c in table.columns]
        self.stdout.write(f"\nsanity {season}: mean percentile by true archetype (qualified only)")
        self.stdout.write(table.to_string())

        misses = []
        for arch, col in SIGNATURES:
            if arch in table.index:
                top2 = table[col].nlargest(2).index
                if arch not in top2:
                    misses.append(f"{arch} is not top-2 on {col}")
        if misses:
            for m in misses:
                self.stdout.write(self.style.WARNING(f"  [WARN] {m}"))
        else:
            self.stdout.write(self.style.SUCCESS("  [OK] every archetype is top-2 on its signature"))

        sh_path = dump / f"shares_{season}.csv"
        if sh_path.exists():
            sh = pd.read_csv(sh_path).merge(truth, on="player_id")
            sh = sh[sh["player_id"].isin(df["player_id"])]          # qualified only
            t2 = sh.groupby("archetype")[["lead", "lead2", "inside", "inside2", "front"]].mean().round(2)
            self.stdout.write(f"\nsanity {season}: mean teammate share by true archetype (qualified only)")
            self.stdout.write(t2.to_string())
            checks = [("Floor General", "lead"), ("UGA Big", "inside"), ("Traditional Big", "inside")]
            for arch, col in checks:
                if arch in t2.index and arch not in t2[col].nlargest(2).index:
                    self.stdout.write(self.style.WARNING(f"  [WARN] {arch} is not top-2 on {col}"))

    # ------------------------------------------------------------------------

    def _pass(self, name):
        self.stdout.write(self.style.SUCCESS(f"  [PASS] {name}"))
        return True

    def _fail(self, name, why=""):
        self.stdout.write(self.style.ERROR(f"  [FAIL] {name} {why}".rstrip()))
        return False
