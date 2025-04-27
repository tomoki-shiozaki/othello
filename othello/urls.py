from django.urls import path

from . import views
from .views import (
    AuthenticatedLocalMatchListView,
    AuthenticatedLocalMatchPlayView,
    AuthenticatedLocalMatchDeleteView,
    AuthenticatedLocalMatchCreateView,
)

urlpatterns = [
    # ログインユーザーが過去のローカル対局記録を確認するためのURL
    path(
        "local/",
        AuthenticatedLocalMatchListView.as_view(),
        name="local_match_list",
    ),
    path(
        "local/new/",
        AuthenticatedLocalMatchCreateView.as_view(),
        name="local_match_new",
    ),
    path(
        "local/<int:pk>/delete/",
        AuthenticatedLocalMatchDeleteView.as_view(),
        name="local_match_delete",
    ),
    # プレイ画面
    path(
        "local/<int:pk>/play/",
        AuthenticatedLocalMatchPlayView.as_view(),
        name="local_match_play",
    ),
    path(
        "local/place-piece/",
        views.AuthenticatedLocalMatchPlacePieceView.as_view(),
        name="place-piece",
    ),
    path("pass_turn/", views.pass_turn, name="pass_turn"),
    path("end-game/", views.end_game_view, name="end_game"),
]
