from django.urls import path

from .views import RolePlayerDetailView, RolePlayerListView

urlpatterns = [
    path("role/players", RolePlayerListView.as_view(), name="role-player-list"),
    path("role/players/<int:player_id>/", RolePlayerDetailView.as_view(),
         name="role-player-detail"),
]