from django.test import TestCase
from django.http import HttpRequest
from django.http import Http404

from apps.guest_games.views import GuestGameSessionMixin


class TestGuestGameSessionMixin(TestCase):
    def setUp(self):
        class DummyView(GuestGameSessionMixin):
            pass

        self.view = DummyView()

    def make_request_with_session(self, guest_game_data):
        request = HttpRequest()
        request.session = {}
        if guest_game_data is not None:
            request.session["guest_game"] = guest_game_data
        return request

    def test_get_guest_game_success(self):
        valid_game = {
            "board": [["empty" for _ in range(8)] for _ in range(8)],
            "turn": "black's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(valid_game)
        game = self.view.get_guest_game(request)
        self.assertEqual(game, valid_game)

    def test_get_guest_game_missing_session(self):
        request = self.make_request_with_session(None)
        with self.assertRaises(Http404):
            self.view.get_guest_game(request)

    def test_get_guest_game_not_a_dict(self):
        request = self.make_request_with_session("not a dict")
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)

    def test_get_guest_game_invalid_board_shape(self):
        invalid_board = [["" for _ in range(7)] for _ in range(8)]
        game = {
            "board": invalid_board,
            "turn": "black's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)

    def test_get_guest_game_board_row_not_list(self):
        game = {
            "board": [["" for _ in range(8)] for _ in range(7)]
            + [None],  # 最後の行がNone
            "turn": "black's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)

    def test_get_guest_game_invalid_cell_type(self):
        board = [[0 for _ in range(8)] for _ in range(8)]  # 数値セル
        game = {
            "board": board,
            "turn": "black's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)

    def test_get_guest_game_invalid_board_cell_value(self):
        invalid_board = [["empty" for _ in range(8)] for _ in range(8)]
        # ある1つのセルに不正値を入れる
        invalid_board[0][0] = "invalid_piece"
        game = {
            "board": invalid_board,
            "turn": "black's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError) as cm:
            self.view.get_guest_game(request)
        self.assertIn("Invalid board cell value", str(cm.exception))

    def test_get_guest_game_invalid_turn(self):
        game = {
            "board": [["" for _ in range(8)] for _ in range(8)],
            "turn": "red's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)

    def test_get_guest_game_invalid_players(self):
        game = {
            "board": [["" for _ in range(8)] for _ in range(8)],
            "turn": "black's turn",
            "black_player": None,
            "white_player": "Bob",
            "result": "対局中",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)

    def test_get_guest_game_invalid_result(self):
        game = {
            "board": [["" for _ in range(8)] for _ in range(8)],
            "turn": "black's turn",
            "black_player": "Alice",
            "white_player": "Bob",
            "result": "unknown",
        }
        request = self.make_request_with_session(game)
        with self.assertRaises(ValueError):
            self.view.get_guest_game(request)
