"""
Run the Role pipeline.

    python manage.py run_role                          # every step built so far, all seasons
    python manage.py run_role --season 2026            # only these seasons (repeat for more)
    python manage.py run_role --steps pooling,play_types --season 2026 --dump-dir dumps

Steps, in run order:
    possessions   -> PlayerSeasonPossessions   (Step 1, saved to DB)
    assist_share  -> NationalAssistShare       (Step 2, saved to DB)
    pooling       -> in memory                 (Step 3: qualified + pooled counts)
    play_types    -> in memory                 (Step 4: play types, rates, percentiles)
    shares        -> PlayerOnfloorShares       (Step 5: lead, lead2, inside, inside2, front)
    placement     -> PlayerGroupScore          (Step 6: group scores + proposed role per group)
                     RolePlacement             (Steps 7-8: guardrails, tiebreakers, final role)

In-memory steps have no table. Use --dump-dir to write them as CSV and look at them:
    dumps/pooled_<season>.csv
    dumps/pooled_three_season_<season>.csv
    dumps/play_types_<season>.csv
    dumps/play_types_three_season_<season>.csv
    dumps/shares_<season>.csv                (Step 5 is saved to the DB too)
    dumps/group_scores_<season>.csv          (Step 6, also in the DB)
    dumps/placements_<season>.csv            (Steps 7-8, also in the DB)

If you ask for a step that needs an in-memory step you did not list (play_types needs
pooling, shares needs play_types, placement needs shares), the needed step runs automatically. DB steps never run automatically:
they read what is already in the database.

Each DB step replaces its own rows for the chosen seasons, so re-running is safe.
"""
import time
from pathlib import Path

import pandas as pd

from django.core.management.base import BaseCommand, CommandError

from ...role_pipeline import loaders
from ...role_pipeline.assist_share import national_assist_share
from ...role_pipeline.groups import GROUP_NAMES, compute_group_scores
from ...role_pipeline.placement import compute_placements
from ...role_pipeline.play_types import compute_play_types, rules_mode
from ...role_pipeline.pooling import pool_season, pool_three_season
from ...role_pipeline.possessions import count_player_possessions
from ...role_pipeline.shares import compute_shares

STEPS = ["possessions", "assist_share", "pooling", "play_types", "shares", "placement"]
NEEDS = {"play_types": ["pooling"], "shares": ["play_types"], "placement": ["shares"]}


class Command(BaseCommand):
    help = "Run the Role (Step 1) pipeline."

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, action="append",
                            help="season to process; repeat for several (default: all)")
        parser.add_argument("--steps", default=",".join(STEPS),
                            help=f"comma-separated, from: {', '.join(STEPS)}")
        parser.add_argument("--dump-dir", metavar="DIR",
                            help="write in-memory step results here as CSV")

    def handle(self, *args, **opts):
        seasons = opts["season"] or loaders.all_seasons()
        if not seasons:
            raise CommandError("no games in the database — run seed_role_dummy first")

        steps = {s.strip() for s in opts["steps"].split(",") if s.strip()}
        unknown = steps - set(STEPS)
        if unknown:
            raise CommandError(f"unknown step(s): {', '.join(sorted(unknown))}")
        added = True                                   # pull in in-memory dependencies,
        while added:                                   # and their dependencies too
            before = len(steps)
            for step in list(steps):
                steps.update(NEEDS.get(step, []))
            added = len(steps) > before

        self.dump = Path(opts["dump_dir"]) if opts["dump_dir"] else None
        if self.dump:
            self.dump.mkdir(parents=True, exist_ok=True)

        self.ctx = {}            # results of in-memory steps, shared between steps
        self.stdout.write(f"Seasons: {seasons}")
        for step in STEPS:                             # always run in STEPS order
            if step in steps:
                t0 = time.time()
                msg = getattr(self, f"step_{step}")(seasons)
                self.stdout.write(f"  {step:<13} {msg}  ({time.time() - t0:.1f}s)")
        self.stdout.write(self.style.SUCCESS("Done."))

    # ---- helpers -------------------------------------------------------------

    def _dump(self, df, name):
        if self.dump is not None:
            df.to_csv(self.dump / f"{name}.csv", index=False, float_format="%.6g")

    # ---- Step 1 and 2: saved to the database --------------------------------

    def step_possessions(self, seasons):
        games = loaders.load_games(seasons)
        poss = loaders.load_possessions(seasons)
        result = count_player_possessions(poss, games)
        n = loaders.save_player_season_possessions(result, seasons)
        return f"{n:>6,} rows saved"

    def step_assist_share(self, seasons):
        counts = loaders.load_counts(seasons)
        result = national_assist_share(counts)
        n = loaders.save_national_assist_share(result, seasons)
        return f"{n:>6,} rows saved"

    # ---- Step 3: pooling (in memory) -----------------------------------------

    def step_pooling(self, seasons):
        c = loaders.load_constants()
        self.ctx["pooled"], self.ctx["pooled3"] = {}, {}
        parts = []
        for s in seasons:
            window = [s - 2, s - 1, s]                 # pooling looks back two seasons
            poss = loaders.load_player_possessions(window)
            counts = loaders.load_counts(window)
            torvik = loaders.load_torvik([s])
            if poss[poss["season"] == s].empty:
                raise CommandError(f"no PlayerSeasonPossessions for {s}: run the possessions step")
            self._warn_missing_history(poss, counts, s)

            pooled = pool_season(poss, counts, torvik, s, c)
            pooled3 = pool_three_season(poss, counts, torvik, s, c)
            self.ctx["pooled"][s], self.ctx["pooled3"][s] = pooled, pooled3
            self._dump(pooled, f"pooled_{s}")
            self._dump(pooled3, f"pooled_three_season_{s}")
            parts.append(f"{s}: {len(pooled)} players, {int(pooled['qualified'].sum())} qualified, "
                         f"{int(pooled['read'].sum())} read, {int(pooled['fallback'].sum())} fallback")
        return "\n" + "\n".join(f"      {p}" for p in parts)

    def _warn_missing_history(self, poss, counts, s):
        """Counts exist for an earlier season but its possessions were never computed:
        pooling would silently treat that season as empty."""
        for prev in (s - 1, s - 2):
            if not counts[counts["season"] == prev].empty and poss[poss["season"] == prev].empty:
                self.stdout.write(self.style.WARNING(
                    f"  ! {prev} has counts but no PlayerSeasonPossessions; "
                    f"run: run_role --steps possessions --season {prev}"))

    # ---- Step 4: play types, rates, percentiles (in memory) -----------------

    def step_play_types(self, seasons):
        c = loaders.load_constants()
        games = loaders.load_games(seasons)
        self.ctx["play_types"], self.ctx["play_types3"], self.ctx["mode"] = {}, {}, {}
        parts = []
        for s in seasons:
            mode = rules_mode(s, games)
            national = loaders.load_national_share(s)
            k = c["SHRINK_K"]
            pt = compute_play_types(self.ctx["pooled"][s], national, mode, k)
            # Same calculation on the three-season sample (needed by tiebreaker 4).
            pt3 = compute_play_types(self.ctx["pooled3"][s], national, mode, k)
            self.ctx["play_types"][s], self.ctx["play_types3"][s] = pt, pt3
            self.ctx["mode"][s] = mode
            self._dump(pt, f"play_types_{s}")
            self._dump(pt3, f"play_types_three_season_{s}")
            n_types = sum(col.startswith("pctl_") for col in pt.columns)
            parts.append(f"{s}: {mode} rules, {n_types} play types")
        return "\n" + "\n".join(f"      {p}" for p in parts)

    # ---- Step 5: teammate shares (saved to the database) ---------------------

    def step_shares(self, seasons):
        c = loaders.load_constants()
        games = loaders.load_games(seasons)
        poss = loaders.load_possessions(seasons)
        results = []
        self.ctx["shares"] = {}
        for s in seasons:
            shares = compute_shares(poss, games, self.ctx["play_types"][s], self.ctx["pooled"][s], s,
                                    min_reads=int(c["SHARE_MIN_READS"]),
                                    min_poss=int(c["SHARE_MIN_POSS"]))
            self._dump(shares, f"shares_{s}")
            self.ctx["shares"][s] = shares
            results.append(shares)
        all_shares = pd.concat(results, ignore_index=True)
        n = loaders.save_onfloor_shares(all_shares, seasons)
        with_lead = int(all_shares["lead"].notna().sum())
        return f"{n:>6,} rows saved ({with_lead} with a lead share, the rest under 200 possessions)"

    # ---- Steps 6-8: group scores, proposals, final role (saved to the database) ---

    def step_placement(self, seasons):
        c = loaders.load_constants()
        all_scores, all_places = [], []
        for s in seasons:
            mode = self.ctx["mode"][s]

            # Step 6a: group raw scores and group scores (this season + three-season sample)
            groups = compute_group_scores(self.ctx["play_types"][s], mode)
            groups3 = compute_group_scores(self.ctx["play_types3"][s], mode)

            # Steps 6b-8: proposals, guardrails, ranking, tiebreakers
            places, proposals = compute_placements(
                self.ctx["pooled"][s], self.ctx["play_types"][s], groups, groups3,
                self.ctx["play_types3"][s], self.ctx["shares"][s], mode, c)
            places["season"] = s

            all_scores.append(self._group_rows(groups, groups3, proposals, s))
            all_places.append(places)
            self._dump(groups, f"group_scores_{s}")
            self._dump(places, f"placements_{s}")

        scores = pd.concat(all_scores, ignore_index=True)
        places = pd.concat(all_places, ignore_index=True)
        n1 = loaders.save_group_scores(scores, seasons)
        n2 = loaders.save_role_placements(places, seasons)
        close = (places["decided_by"].isin(
            ["creator", "interior", "length", "larger_sample", "volume"])).mean()
        return (f"{n1:>6,} group-score rows, {n2:,} placements saved "
                f"({close:.0%} decided by a tiebreaker)")

    @staticmethod
    def _group_rows(groups, groups3, proposals, season):
        """Wide group tables -> one row per player x group x sample, for PlayerGroupScore."""
        rows = []
        for sample, df in (("current", groups), ("three_season", groups3)):
            for g in GROUP_NAMES:
                part = df[["player_id"]].copy()
                part["group_name"] = g
                part["sample"] = sample
                part["raw_score"] = df[f"raw_{g}"]
                part["group_score"] = df[f"score_{g}"]
                rows.append(part)
        out = pd.concat(rows, ignore_index=True)
        out["season"] = season
        prop = proposals.assign(sample="current")
        out = out.merge(prop, on=["player_id", "group_name", "sample"], how="left")
        return out[["player_id", "season", "group_name", "sample",
                    "raw_score", "group_score", "proposed_role"]]
