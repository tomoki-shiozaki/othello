from django.test import TestCase
from django.urls import reverse, resolve
import json

from apps.guest_games.views import (
    GuestGameHomeView,
    GuestGameStartView,
    guest_play_view,
)


class TestGuestGameAccess(TestCase):

    def test_home_url_resolves(self):
        url = reverse("guest_games:home")
        self.assertEqual(resolve(url).func.view_class, GuestGameHomeView)

    def test_new_url_resolves(self):
        url = reverse("guest_games:new")
        self.assertEqual(resolve(url).func.view_class, GuestGameStartView)

    def test_play_url_resolves(self):
        url = reverse("guest_games:play")
        self.assertEqual(resolve(url).func, guest_play_view)

    def test_home_url_returns_200(self):
        response = self.client.get(reverse("guest_games:home"))
        self.assertEqual(response.status_code, 200)

    def test_new_url_returns_200(self):
        response = self.client.get(reverse("guest_games:new"))
        self.assertEqual(response.status_code, 200)

    def test_play_url_returns_200(self):
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

    def test_place_piece_url_returns_200(self):
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": [["empty"] * 8 for _ in range(8)],
            "result": "対局中",
        }
        session.save()

        response = self.client.post(
            reverse("guest_games:place_piece"),
            data=json.dumps({"cell": 0}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_pass_turn_url_returns_200(self):
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": [["empty"] * 8 for _ in range(8)],
            "result": "対局中",
        }
        session.save()

        response = self.client.post(
            reverse("guest_games:pass_turn"),
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_end_game_url_returns_200(self):
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": [["empty"] * 8 for _ in range(8)],
            "result": "対局中",
        }
        session.save()

        response = self.client.post(
            reverse("guest_games:end_game"),
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
