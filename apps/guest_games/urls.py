from django.urls import path

from apps.guest_games.views import (
    GuestGameHomeView,
    GuestGameStartView,
    GuestGamePlayView,
    GuestGamePlacePieceView,
    GuestGamePassTurnView,
    GuestGameEndView,
)

app_name = "guest_games"

urlpatterns = [
    path("", GuestGameHomeView.as_view(), name="home"),
    path("new/", GuestGameStartView.as_view(), name="new"),
    path("play/", GuestGamePlayView.as_view(), name="play"),
    path(
        "play/place-piece/",
        GuestGamePlacePieceView.as_view(),
        name="place_piece",
    ),
    path("play/pass-turn/", GuestGamePassTurnView.as_view(), name="pass_turn"),
    path("play/end-game/", GuestGameEndView.as_view(), name="end_game"),
]
