"""
Seed the Role models with dummy data.

Place this file at:   <your_app>/management/commands/seed_role_dummy.py
and dummy_data.py at: <your_app>/dummy_data.py

Usage:
    python manage.py seed_role_dummy                 # seed (refuses if data already exists)
    python manage.py seed_role_dummy --flush         # wipe ALL role tables, then seed
    python manage.py seed_role_dummy --seed 7        # a different random dataset
    python manage.py seed_role_dummy --flush --check-dir checks
        # also writes the answer keys for verifying your pipeline:
        #   checks/expected_possessions.csv   (player_id, season, off_poss, def_poss, tagged_off_poss)
        #   checks/expected_assist_share.csv  (season, zone, ast_share)
        # then:  python manage.py verify_role_steps --check-dir checks

Seeds SOURCE tables only:
    Team, Player, Game, Possession, PlayerSeasonCounts, TorvikPlayerSeason,
    ModelConstant, DummyTruth
Leaves DERIVED and OUTPUT tables empty — your pipeline fills them:
    PlayerSeasonPossessions, NationalAssistShare,
    PlayerOnfloorShares, PlayerGroupScore, RolePlacement
"""
import math
import time
from pathlib import Path
from decimal import Decimal

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import models as djm, transaction

from ...dummy_data import generate
from ...models import (
    DummyTruth, Game, ModelConstant, NationalAssistShare, Player, PlayerGroupScore,
    PlayerOnfloorShares, PlayerSeasonCounts, PlayerSeasonPossessions, Possession,
    RolePlacement, Team, TorvikPlayerSeason,
)

# Load order (parents first). Flush runs in reverse.
LOAD = [
    ("teams", Team),
    ("players", Player),
    ("games", Game),
    ("possessions", Possession),
    ("player_season_counts", PlayerSeasonCounts),
    ("torvik_player_season", TorvikPlayerSeason),
    ("dummy_truth", DummyTruth),
    ("model_constants", ModelConstant),
]
DERIVED_AND_OUTPUT = [RolePlacement, PlayerGroupScore, PlayerOnfloorShares,
                      NationalAssistShare, PlayerSeasonPossessions]

BATCH = 5000


def _is_missing(v):
    if v is None or v is pd.NA or v is pd.NaT:
        return True
    return isinstance(v, float) and math.isnan(v)


def _converter(model, column):
    """Return a function that turns a pandas/numpy value into what the field expects."""
    # DataFrame columns are attnames: FK `player` -> `player_id`, FK `game` -> `game_id`
    field = next(f for f in model._meta.concrete_fields if f.attname == column)

    if isinstance(field, djm.DecimalField):
        places = field.decimal_places
        return lambda v: None if _is_missing(v) else Decimal(str(round(float(v), places)))
    if isinstance(field, djm.BooleanField):
        return lambda v: None if _is_missing(v) else bool(v)
    if isinstance(field, (djm.IntegerField, djm.ForeignKey)):   # Small/Big/Integer + FKs
        return lambda v: None if _is_missing(v) else int(v)
    if isinstance(field, djm.DateField) and not isinstance(field, djm.DateTimeField):
        return lambda v: None if _is_missing(v) else (v.date() if isinstance(v, pd.Timestamp) else v)
    return lambda v: None if _is_missing(v) else (v.item() if isinstance(v, np.generic) else v)


def _objects(model, df):
    cols = list(df.columns)
    conv = [_converter(model, c) for c in cols]
    for rec in df.itertuples(index=False, name=None):
        yield model(**{c: f(v) for c, f, v in zip(cols, conv, rec)})


class Command(BaseCommand):
    help = "Seed the Role (Step 1) source tables with dummy data."

    def add_arguments(self, parser):
        parser.add_argument("--seed", type=int, default=42, help="random seed (default 42)")
        parser.add_argument("--flush", action="store_true",
                            help="delete everything in all role tables before seeding")
        parser.add_argument("--check-dir", metavar="DIR",
                            help="write answer-key CSVs here for verifying your pipeline")

    def handle(self, *args, **opts):
        if Player.objects.exists() and not opts["flush"]:
            raise CommandError("Data already present. Re-run with --flush to wipe and reseed.")

        t0 = time.time()
        self.stdout.write(f"Generating dummy data (seed={opts['seed']}) ...")
        frames = generate(seed=opts["seed"])

        with transaction.atomic():
            if opts["flush"]:
                for model in DERIVED_AND_OUTPUT + [m for _, m in reversed(LOAD)]:
                    n, _ = model.objects.all().delete()
                    if n:
                        self.stdout.write(f"  flushed {model.__name__}: {n}")

            for key, model in LOAD:
                df = frames[key]
                objs = list(_objects(model, df))
                for i in range(0, len(objs), BATCH):
                    model.objects.bulk_create(objs[i:i + BATCH])
                self.stdout.write(f"  {model.__name__:<22} {len(objs):>7,} rows")

        if opts["check_dir"]:
            out = Path(opts["check_dir"])
            out.mkdir(parents=True, exist_ok=True)
            # Int64 keeps tagged_off_poss as a whole number with blanks for pre-2026
            frames["_check_possessions"].astype({"tagged_off_poss": "Int64"}) \
                .to_csv(out / "expected_possessions.csv", index=False)
            frames["_check_assist_share"].to_csv(out / "expected_assist_share.csv", index=False)
            self.stdout.write(f"  answer keys -> {out}/expected_possessions.csv, "
                              f"{out}/expected_assist_share.csv")

        self.stdout.write(self.style.SUCCESS(f"Done in {time.time() - t0:.1f}s. "
                                             "Derived and output tables are empty."))
