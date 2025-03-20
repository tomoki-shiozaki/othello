from django.urls import path

from . import views

urlpatterns = [
    # 新しいゲームを開始するためのURL
    path('start_new_game/', views.start_new_game, name='start_new_game'),
    # ゲーム進行管理ページ（トップページ）
    path('', views.home, name='home'), 
    #オセロの駒を打つリクエスト
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    #ターンをパスするリクエスト
    path('pass_turn/', views.pass_turn, name='pass_turn'),
]
