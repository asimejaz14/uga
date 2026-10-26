"""
Role API — two read-only endpoints.

GET /api/role/players/
    List of players with their role for one season.
    Query parameters (all optional):
        season      default: the latest season that has placements
        role        exact primary role, e.g. "Floor General"
        family      Guards | Wings | Bigs
        confidence  normal | low
        search      part of the player's name (case-insensitive)
        page        page number (page size: PAGE_SIZE below, or ?page_size=)

GET /api/role/players/<player_id>/
    One player, every season: role, secondary role, family, confidence, the audit
    trail, height, teammate shares and the seven group scores.
"""
from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Player, PlayerGroupScore, PlayerOnfloorShares, RolePlacement,
                     TorvikPlayerSeason)
from .serializers import RoleListItemSerializer, SeasonRoleSerializer

SPEC_VERSION = "9.1"     # which model version to show


class RolePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"      # ?page_size=50
    max_page_size = 200


class RolePlayerListView(APIView):
    """GET: paginated player list with role attributes for one season."""

    def get(self, request):
        placements = RolePlacement.objects.filter(spec_version=SPEC_VERSION)

        # --- which season: ?season=2026, or the latest one we have ---------------
        season = request.query_params.get("season")
        if season is None:
            season = placements.aggregate(latest=Max("season"))["latest"]
        elif not season.isdigit():
            return Response({"detail": "season must be a year, e.g. 2026"}, status=400)
        if season is None:                                   # no placements at all yet
            return Response({"season": None, "count": 0, "next": None,
                             "previous": None, "results": []})
        placements = placements.filter(season=int(season))

        # --- optional filters ---------------------------------------------------
        params = request.query_params
        if params.get("role"):
            placements = placements.filter(primary_role=params["role"])
        if params.get("family"):
            placements = placements.filter(family=params["family"])
        if params.get("confidence"):
            placements = placements.filter(confidence=params["confidence"])
        if params.get("search"):
            placements = placements.filter(player__player_name__icontains=params["search"])

        # select_related: fetch the player's name in the same query (no N+1)
        placements = placements.select_related("player").order_by("player__player_name",
                                                                   "player_id")

        # --- paginate -------------------------------------------------------------
        paginator = RolePagination()
        page = paginator.paginate_queryset(placements, request, view=self)
        data = RoleListItemSerializer(page, many=True).data
        response = paginator.get_paginated_response(data)
        response.data["season"] = int(season)
        return response


class RolePlayerDetailView(APIView):
    """GET: one player, all seasons, newest first."""

    def get(self, request, player_id):
        player = get_object_or_404(Player, player_id=player_id)

        placements = (RolePlacement.objects
                      .filter(player_id=player_id, spec_version=SPEC_VERSION)
                      .order_by("-season"))

        # Everything else is fetched ONCE per table and grouped by season,
        # then handed to the serializer through `context`.
        heights = {
            t.season: float(t.height_in) if t.height_in is not None else None
            for t in TorvikPlayerSeason.objects.filter(player_id=player_id)
        }

        def num(v):
            return float(v) if v is not None else None

        shares = {
            s.season: {"valid_poss": s.valid_poss, "lead": num(s.lead), "lead2": num(s.lead2),
                       "inside": num(s.inside), "inside2": num(s.inside2), "front": num(s.front)}
            for s in PlayerOnfloorShares.objects.filter(player_id=player_id)
        }

        group_scores = {}
        for g in (PlayerGroupScore.objects
                  .filter(player_id=player_id, sample="current")
                  .order_by("season", "-group_score")):
            group_scores.setdefault(g.season, []).append({
                "group": g.group_name,
                "raw_score": num(g.raw_score),
                "group_score": num(g.group_score),
                "proposed_role": g.proposed_role,
            })

        context = {"heights": heights, "shares": shares, "group_scores": group_scores}
        return Response({
            "player_id": player.player_id,
            "player_name": player.player_name,
            "seasons": SeasonRoleSerializer(placements, many=True, context=context).data,
        })