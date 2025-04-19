from django.urls import path

from . import views
from .views import (
    AuthenticatedLocalMatchListView,
    AuthenticatedLocalMatchPlayView,
    # AuthenticatedLocalMatchDetailView,
    # AuthenticatedLocalMatchDeleteView,
)

urlpatterns = [
    # 対局履歴から、プレイ画面に移動するURL
    path(
        "local/<int:pk>/play/",
        AuthenticatedLocalMatchPlayView.as_view(),
        name="local_match_play",
    ),
    # path(
    #     "local/<int:pk>/",
    #     AuthenticatedLocalMatchDetailView.as_view(),
    #     name="local_match_detail",
    # ),
    # path(
    #     "local/<int:pk>/delete/",
    #     AuthenticatedLocalMatchDeleteView.as_view(),
    #     name="local_match_delete",
    # ),
    # ログインユーザーが過去のローカル対局記録を確認するためのURL
    path(
        "local/",
        AuthenticatedLocalMatchListView.as_view(),
        name="local_match_list",
    ),
    # 新しいゲームを開始するためのURL
    path("start_new_game/", views.start_new_game, name="start_new_game"),
    # ゲーム進行管理ページ（トップページ）
    # path("", views.home, name="home"),
    path("local/authenticated/", views.local_match, name="authenticated_local_match"),
    # オセロの駒を打つビュー
    path(
        "local/place-piece/",
        views.place_piece_view,
        name="place-piece",
    ),
    # # オセロの駒を打つビュー
    # path("fetch_data/", views.place_piece_view, name="fetch_data"),
    # ターンをパスするリクエスト
    path("pass_turn/", views.pass_turn, name="pass_turn"),
]
