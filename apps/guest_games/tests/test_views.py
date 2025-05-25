from django.test import TestCase
from django.urls import reverse


class TestGuestGameHomeView(TestCase):
    def test_get_renders_template(self):
        response = self.client.get(reverse("guest_games:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "guest_games/guest_game_home.html")


class TestGuestGameStartView(TestCase):
    def test_get_renders_template(self):
        response = self.client.get(reverse("guest_games:new"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "guest_games/guest_game_new.html")

    def test_post_valid_data_sets_session_and_redirects(self):
        data = {
            "black_player": "たろう",
            "white_player": "はなこ",
        }
        response = self.client.post(reverse("guest_games:new"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("guest_games:play"))

        session_game = self.client.session.get("guest_game")
        self.assertIsNotNone(session_game)
        self.assertEqual(session_game["black_player"], "たろう")
        self.assertEqual(session_game["white_player"], "はなこ")


class TestGuestPlayView(TestCase):
    def test_redirects_if_no_session(self):
        response = self.client.get(reverse("guest_games:play"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("guest_games:new"))

    def test_with_session_renders_template(self):
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": [["empty"] * 8 for _ in range(8)],
            "result": "対局中",
        }
        session.save()

        response = self.client.get(reverse("guest_games:play"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "guest_games/guest_game_play.html")
        self.assertIn("game", response.context)
        self.assertEqual(response.context["game"]["black_player"], "たろう")
