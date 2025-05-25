from django.urls import path

from apps.guest_games.views import (
    GuestGameHomeView,
    GuestGameStartView,
    GuestGamePlacePieceView,
    GuestGamePassTurnView,
    GuestGameEndView,
)
from apps.guest_games.views import guest_play_view

app_name = "guest_games"

urlpatterns = [
    path("", GuestGameHomeView.as_view(), name="home"),
    path("new/", GuestGameStartView.as_view(), name="new"),
    path("play/", guest_play_view, name="play"),
    path(
        "play/place-piece/",
        GuestGamePlacePieceView.as_view(),
        name="place-piece",
    ),
    path("play/pass-turn/", GuestGamePassTurnView.as_view(), name="pass_turn"),
    path("play/end-game/", GuestGameEndView.as_view(), name="end_game"),
]
