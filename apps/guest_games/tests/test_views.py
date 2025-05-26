from django.test import TestCase
from django.urls import reverse
import json
from unittest.mock import patch
import logging


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


class TestGuestGamePlacePieceView(TestCase):
    def setUp(self):
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": [["empty"] * 8 for _ in range(8)],
            "result": "対局中",
        }
        session.save()
        self.url = reverse("guest_games:place_piece")

    def test_game_session_not_found_returns_404(self):
        # セッションに guest_game を設定しない
        session = self.client.session
        if "guest_game" in session:
            del session["guest_game"]
        session.save()

        response = self.client.post(
            self.url,
            data=json.dumps({"cell": 10}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Game session not found"})

    @patch("apps.guest_games.views.Rule")  # Rule をモックする
    def test_place_piece_successfully(self, MockRule):
        # モックの設定
        mock_rule_instance = MockRule.return_value
        mock_rule_instance.find_reversable_pieces.return_value = {
            "can_place_piece": True,
            "reversable_pieces": [(3, 4)],
        }
        mock_rule_instance.board = [["dummy"] * 8 for _ in range(8)]
        mock_rule_instance.turn = "white's turn"

        # POSTリクエスト
        data = {"cell": 20}
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

        # 結果の検証
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("board", json_data)
        self.assertIn("turn", json_data)
        self.assertEqual(json_data["turn"], "white's turn")
        mock_rule_instance.place_and_reverse_pieces.assert_called_once()

    # 駒が置けない場合
    @patch("apps.guest_games.views.Rule")
    def test_place_piece_not_allowed(self, MockRule):
        mock_rule_instance = MockRule.return_value
        mock_rule_instance.find_reversable_pieces.return_value = {
            "can_place_piece": False,
            "reversable_pieces": [],
        }

        mock_rule_instance.board = [["dummy"] * 8 for _ in range(8)]
        mock_rule_instance.turn = "black's turn"

        data = {"cell": 28}
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["turn"], "black's turn")  # ターンが変わらない
        self.assertEqual(json_data["board"][0][0], "empty")
        mock_rule_instance.place_and_reverse_pieces.assert_not_called()

    def test_place_piece_invalid_cell(self):
        # 無効なセル（例えば、盤面外の座標など）を送信
        response = self.client.post(
            self.url,
            data=json.dumps({"cell": 64}),  # 盤面外
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_place_piece_cell_not_integer(self):
        # 無効なセル（セルが整数でない）を送信
        response = self.client.post(
            self.url,
            data=json.dumps({"cell": "not an int"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_place_piece_cell_missing(self):
        response = self.client.post(
            self.url,
            data=json.dumps({}),  # "cell" キーがない
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_invalid_json_returns_400(self):
        response = self.client.post(
            self.url,
            data="invalid json",  # JSONではない文字列
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid JSON"})

    @patch("apps.guest_games.views.Rule")
    def test_place_piece_rule_exception(self, MockRule):
        # ロギングを一時的に無効化
        logging.disable(logging.CRITICAL)
        MockRule.side_effect = Exception("unexpected error")

        response = self.client.post(
            self.url,
            data=json.dumps({"cell": 20}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"], "Internal server error")

        # ロギングを有効化
        logging.disable(logging.NOTSET)


class TestGuestGamePassTurnView(TestCase):
    def setUp(self):
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": [["empty"] * 8 for _ in range(8)],
            "result": "対局中",
        }
        session.save()
        self.url = reverse("guest_games:pass_turn")

    def test_pass_turn_black_to_white(self):
        response = self.client.post(self.url)
        session = self.client.session
        game_data = session.get("guest_game")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(game_data["turn"], "white's turn")
        self.assertEqual(response.json()["message"], "Player passed.")
        self.assertEqual(response.json()["turn"], "white's turn")

    def test_pass_turn_white_to_black(self):
        session = self.client.session
        game_data = session.get("guest_game")
        game_data["turn"] = "white's turn"
        session["guest_game"] = game_data
        session.save()

        response = self.client.post(self.url)
        session = self.client.session
        game_data = session.get("guest_game")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(game_data["turn"], "black's turn")
        self.assertEqual(response.json()["message"], "Player passed.")
        self.assertEqual(response.json()["turn"], "black's turn")


class TestGuestEndGameView(TestCase):
    def setUp(self):
        self.board_data = [["empty"] * 8 for _ in range(8)]
        session = self.client.session
        session["guest_game"] = {
            "black_player": "たろう",
            "white_player": "はなこ",
            "turn": "black's turn",
            "board": self.board_data,
            "result": "対局中",
        }
        session.save()
        self.url = reverse("guest_games:end_game")

    @patch("apps.guest_games.views.end_game")
    def test_end_game_black_wins(self, mock_end_game):
        # モックの設定
        mock_end_game.return_value = {
            "blackCount": 40,
            "whiteCount": 24,
            "winner": "black",
        }

        response = self.client.post(self.url)
        session = self.client.session
        game_data = session.get("guest_game")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(game_data["result"], "black")  # セッションの更新確認
        self.assertEqual(response.json()["blackCount"], 40)
        self.assertEqual(response.json()["whiteCount"], 24)
        self.assertEqual(response.json()["winner"], "black")
        mock_end_game.assert_called_once_with(self.board_data)

    @patch("apps.guest_games.views.end_game")
    def test_end_game_draw(self, mock_end_game):
        mock_end_game.return_value = {
            "blackCount": 32,
            "whiteCount": 32,
            "winner": "draw",
        }

        # 偽のボードをセッションに再設定
        fake_board = [["black"] * 4 + ["white"] * 4] * 8
        session = self.client.session
        game_data = session["guest_game"]
        game_data["board"] = fake_board
        session["guest_game"] = game_data
        session.save()

        response = self.client.post(self.url)
        session = self.client.session
        game_data = session.get("guest_game")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(game_data["result"], "draw")
        self.assertEqual(response.json()["blackCount"], 32)
        self.assertEqual(response.json()["whiteCount"], 32)
        self.assertEqual(response.json()["winner"], "draw")
        mock_end_game.assert_called_once_with(fake_board)
