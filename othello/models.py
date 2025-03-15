from django.db import models

# Create your models here.
class Game(models.Model):
    turn=models.CharField(max_length=10) #'black's turn', 'white's turn'
    board=models.JSONField()

    def __str__(self):
        return f"Game with turn: {self.turn}"

