from django.urls import path

from . import views

urlpatterns = [
    # 新しいゲームを開始するためのURL
    path("start_new_game/", views.start_new_game, name="start_new_game"),
    # ゲーム進行管理ページ（トップページ）
    # path("", views.home, name="home"),
    path("match/local/", views.local_match, name="local-match"),
    # オセロの駒を打つビュー
    path("fetch_data/", views.place_piece_view, name="fetch_data"),
    # ターンをパスするリクエスト
    path("pass_turn/", views.pass_turn, name="pass_turn"),
]
