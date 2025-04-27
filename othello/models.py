from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
# オセロのゲームモデル
# 盤面の初期状態を定義
def default_settings():
    initial_board = []
    for _ in range(8):
        initial_board.append(["empty"] * 8)
    initial_board[3][3] = "black"
    initial_board[4][4] = "black"
    initial_board[3][4] = "white"
    initial_board[4][3] = "white"
    return initial_board


# ログインユーザーのローカル対戦用のゲームモデル
class AuthenticatedLocalMatch(models.Model):
    authenticated_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    black_player = models.CharField(
        max_length=255,
        verbose_name="黒のプレイヤー",
    )
    white_player = models.CharField(
        max_length=255,
        verbose_name="白のプレイヤー",
    )
    #'black's turn', 'white's turn'の２つを設定
    turn = models.CharField(max_length=15, default="black's turn")
    board = models.JSONField(default=default_settings)
    result = models.CharField(max_length=15, default="対局中")

    def __str__(self):
        return f"{self.black_player}と{self.white_player}の対局"

    def get_absolute_url(self):
        return reverse("local_match_play", args=[str(self.id)])
