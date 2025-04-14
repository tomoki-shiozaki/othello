from django.db import models


# Create your models here.
def default_settings():
    initial_board = []
    for _ in range(8):
        initial_board.append(["empty"] * 8)
    initial_board[3][3] = "black"
    initial_board[4][4] = "black"
    initial_board[3][4] = "white"
    initial_board[4][3] = "white"
    return initial_board


class Game(models.Model):
    turn = models.CharField(
        max_length=15, default="black's turn"
    )  #'black's turn', 'white's turn'
    board = models.JSONField(default=default_settings)

    def __str__(self):
        return f"Game with turn: {self.turn}"
