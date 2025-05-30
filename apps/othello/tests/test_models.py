from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import AuthenticatedLocalMatch


# Create your tests here.
class AuthenticatedLocalMatchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", password="testpass", email="testuser@email.com"
        )
        self.game = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user, black_player="test1", white_player="test2"
        )

    def test_create_game(self):
        game = self.game
        self.assertEqual(AuthenticatedLocalMatch.objects.all().count(), 1)
        self.assertEqual(game.authenticated_user, self.user)
        self.assertEqual(game.black_player, "test1")
        self.assertEqual(game.white_player, "test2")
        self.assertEqual(game.turn, "black's turn")
        self.assertEqual(game.board[3][3], "black")
        self.assertEqual(game.board[3][4], "white")
        self.assertEqual(game.result, "対局中")

    def test_str_representation(self):
        game = self.game
        self.assertEqual(str(game), "test1とtest2の対局")

    def test_get_absolute_url(self):
        game = self.game
        self.assertEqual(
            game.get_absolute_url(), reverse("local_match_play", args=[game.id])
        )
