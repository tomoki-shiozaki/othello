from django.test import TestCase
from apps.guest_games.forms import GuestGameCreationForm


class GuestGameCreationFormTests(TestCase):
    def test_valid_data(self):
        form = GuestGameCreationForm(
            data={
                "black_player": "たろう",
                "white_player": "はなこ",
            }
        )
        self.assertTrue(form.is_valid())

    def test_missing_black_player(self):
        form = GuestGameCreationForm(
            data={
                "black_player": "",
                "white_player": "はなこ",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("black_player", form.errors)

    def test_missing_white_player(self):
        form = GuestGameCreationForm(
            data={
                "black_player": "たろう",
                "white_player": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("white_player", form.errors)

    def test_too_long_name(self):
        long_name = "a" * 300  # 255文字超え
        form = GuestGameCreationForm(
            data={
                "black_player": long_name,
                "white_player": "はなこ",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("black_player", form.errors)
