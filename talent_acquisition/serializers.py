"""
Serializers for the Role API.

RoleListItemSerializer   one row of the player list (name + a few role attributes)
SeasonRoleSerializer     one season of the detail page (everything about that season)
"""
from rest_framework import serializers

from .models import RolePlacement


class RoleListItemSerializer(serializers.ModelSerializer):
    """One player in the list, for one season."""
    # RolePlacement.player_id already holds the external player ID (FK to_field),
    # so it can be read directly; the name comes through the FK.
    player_id = serializers.IntegerField()
    player_name = serializers.CharField(source="player.player_name")

    class Meta:
        model = RolePlacement
        fields = ["player_id", "player_name", "season",
                  "primary_role", "secondary_role", "family", "confidence"]


class SeasonRoleSerializer(serializers.ModelSerializer):
    """One season of one player, with everything Role produced for it.

    Extra data that lives in other tables (height, teammate shares, group scores)
    is looked up in dictionaries the view passes in `context`, keyed by season,
    so the serializer itself never runs a query per row.
    """
    # Decimals -> numbers in JSON (DRF would otherwise send them as strings)
    lead = serializers.FloatField(allow_null=True)
    inside = serializers.FloatField(allow_null=True)

    height_in = serializers.SerializerMethodField()
    onfloor_shares = serializers.SerializerMethodField()
    group_scores = serializers.SerializerMethodField()

    class Meta:
        model = RolePlacement
        fields = [
            "season",
            "primary_role", "secondary_role", "family",
            "confidence", "fallback", "rules_mode", "decided_by",
            "winning_group", "top3_groups", "top4_play_types",
            "pooled_off_poss", "lead", "inside",
            "height_in", "onfloor_shares", "group_scores",
            "spec_version", "computed_at",
        ]

    def get_height_in(self, obj):
        return self.context["heights"].get(obj.season)

    def get_onfloor_shares(self, obj):
        return self.context["shares"].get(obj.season)

    def get_group_scores(self, obj):
        return self.context["group_scores"].get(obj.season, [])