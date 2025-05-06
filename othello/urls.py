from django.urls import path

from . import views
from .views import (
    AuthenticatedLocalMatchListView,
    AuthenticatedLocalMatchPlayView,
    AuthenticatedLocalMatchDeleteView,
    AuthenticatedLocalMatchCreateView,
    AuthenticatedLocalMatchPlacePieceView,
    PassTurnView,
    EndGameView,
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
        "local/<int:pk>/place-piece/",
        AuthenticatedLocalMatchPlacePieceView.as_view(),
        name="place-piece",
    ),
    path("local/<int:pk>/pass-turn/", PassTurnView.as_view(), name="pass_turn"),
    path("local/<int:pk>/end-game/", EndGameView.as_view(), name="end_game"),
]
