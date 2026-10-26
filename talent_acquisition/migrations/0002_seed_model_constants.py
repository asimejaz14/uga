"""
Seeds the v9.1 model constants (previously the INSERT in schema.sql).
Place in talent_acquisition/migrations/ after running `makemigrations role` (which creates 0001_initial).
"""

from django.db import migrations

CONSTANTS = [
    ("MIN_PCT_QUALIFIED",  "40",   "Torvik minutes % for qualified"),
    ("MIN_POSS",           "300",  "offensive possessions for qualified / read"),
    ("PREV_SEASON_WEIGHT", "0.5",  "ROLE_DEF_PREV_W, established players"),
    ("SHRINK_K",           "5",    "assisted-share shrink over 5 makes"),
    ("SHARE_MIN_POSS",     "200",  "min possessions for lead/inside shares"),
    ("SHARE_MIN_READS",    "4",    "4 of the 5 on his side need a read"),
    ("SHARE_THRESHOLD",    "0.50", "lead / inside / front cut"),
    ("DEF_CLOSE",          "0.10", "close-call gap"),
    ("H_WING",             "77",   "6'5\""),
    ("H_67",               "79",   "6'7\""),
    ("H_GUARD_MAX",        "80",   "6'8\""),
    ("THREE_SHARE_SPEC",   "0.60", "shooting rule: 60%+ shots are threes"),
    ("DRB_PCTL_HIGH",      "0.60", "shooting rule 1"),
    ("DRB_PCTL_LOW",       "0.50", "shooting rule 2"),
    ("STEAL_SHOOT_MARGIN", "0.05", "shooting rule 5"),
]


def seed(apps, schema_editor):
    ModelConstant = apps.get_model("talent_acquisition", "ModelConstant")
    for key, value, note in CONSTANTS:
        ModelConstant.objects.update_or_create(
            spec_version="9.1", key=key, defaults={"value": value, "note": note}
        )


def unseed(apps, schema_editor):
    ModelConstant = apps.get_model("talent_acquisition", "ModelConstant")
    ModelConstant.objects.filter(spec_version="9.1", key__in=[c[0] for c in CONSTANTS]).delete()


class Migration(migrations.Migration):
    dependencies = [("talent_acquisition", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
