from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
import json
from unittest.mock import patch
import logging

from ..models import AuthenticatedLocalMatch
from ..views import AuthenticatedLocalMatchListView


class AuthenticatedLocalMatchListViewTest(TestCase):
    def setUp(self):
        # ユーザー作成
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.other_user = get_user_model().objects.create_user(
            username="otheruser", password="otherpassword"
        )

        # テスト用のAuthenticatedLocalMatchを作成
        self.match1 = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user
        )
        self.match2 = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user
        )
        self.match3 = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.other_user
        )

        # テスト用のRequestFactoryを作成
        self.factory = RequestFactory()

    # RequestFactoryベースの単体テスト
    def test_authenticated_user_can_see_their_matches(self):
        # ログインした状態でリクエスト
        request = self.factory.get(reverse("local_match_list"))
        request.user = self.user

        # ビューをシミュレート
        view = AuthenticatedLocalMatchListView()
        view.request = request
        response = view.get(request)

        # 正しいマッチが返されているか確認
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context_data["object_list"],
            [self.match1, self.match2],
            ordered=False,
        )

    def test_authenticated_user_can_see_their_matches_by_client(self):
        """Clientベースの統合テスト"""
        # ログイン処理
        self.client.login(username="testuser", password="testpassword")

        # ログイン状態で GET リクエスト
        response = self.client.get(reverse("local_match_list"))

        # ステータスコードが 200 であることを確認
        self.assertEqual(response.status_code, 200)

        # 自分のマッチだけが表示されていることを確認
        self.assertQuerySetEqual(
            response.context["object_list"], [self.match1, self.match2], ordered=False
        )

    def test_authenticated_user_cannot_see_other_users_matches(self):
        # ログインした状態でリクエスト
        request = self.factory.get(reverse("local_match_list"))
        request.user = self.user

        # ビューをシミュレート
        view = AuthenticatedLocalMatchListView()
        view.request = request
        response = view.get(request)

        # 他のユーザーのマッチは返されない
        self.assertNotIn(self.match3, response.context_data["object_list"])

    def test_authenticated_user_cannot_see_other_users_matches_by_client(self):
        """Clientベースの統合テスト"""
        # ログイン処理
        self.client.login(username="testuser", password="testpassword")

        # ログイン状態で GET リクエスト
        response = self.client.get(reverse("local_match_list"))

        # 他のユーザーのゲームが表示されていないことを確認
        self.assertNotIn(self.match3, response.context_data["object_list"])

    def test_view_uses_correct_template(self):
        """ビューが正しいテンプレートを使っているか確認"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("local_match_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "match/local/list.html")


class TestOwnerLoginMixin:
    def login_user(self, username="testuser", password="testpassword"):
        user = get_user_model().objects.create_user(
            username=username, password=password
        )
        self.client.login(username=username, password=password)
        return user


class AuthenticatedLocalMatchCreateViewTest(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.create_url = reverse("local_match_new")

    def test_create_match_success(self):
        response = self.client.post(
            self.create_url,
            {
                "black_player": "Alice",
                "white_player": "Bob",
            },
        )

        # リダイレクトされているか（CreateViewの成功時）
        self.assertEqual(response.status_code, 302)

        # 作成されたオブジェクトを確認
        match = AuthenticatedLocalMatch.objects.first()
        self.assertIsNotNone(match)
        self.assertEqual(match.black_player, "Alice")
        self.assertEqual(match.white_player, "Bob")
        self.assertEqual(match.authenticated_user, self.user)

    def test_uses_correct_template(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "match/local/new.html")

    def test_invalid_form(self):
        # 空フォーム送信（black_player, white_playerともに入力必須。バリデーションエラーが起こる）
        response = self.client.post(self.create_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "black_player", "このフィールドは必須です。"
        )
        self.assertFormError(
            response.context["form"], "white_player", "このフィールドは必須です。"
        )


class AuthenticatedLocalMatchDeleteViewTest(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )
        self.delete_url = reverse("local_match_delete", args=[self.match.pk])

    def test_delete_view_uses_correct_template(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "match/local/delete.html")

    def test_post_deletes_object(self):
        self.assertEqual(AuthenticatedLocalMatch.objects.count(), 1)
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse("local_match_list"))
        self.assertEqual(AuthenticatedLocalMatch.objects.count(), 0)


class AuthenticatedLocalMatchPlayViewTest(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )
        self.play_url = reverse("local_match_play", args=[self.match.pk])

    def test_play_view_uses_correct_template_and_context(self):
        response = self.client.get(self.play_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "match/local.html")
        self.assertEqual(response.context["match"], self.match)

        # board は JSON 形式で context に含まれる
        board_json = json.dumps(self.match.board)
        self.assertEqual(response.context["board"], board_json)


class AuthenticatedLocalMatchPlacePieceViewTest(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )
        self.url = reverse("place_piece", args=[self.match.pk])

    @patch("apps.othello.views.Rule")  # Rule をモックする
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
    @patch("apps.othello.views.Rule")
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

    @patch("apps.othello.views.Rule")
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


class PassTurnViewViewTest(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )
        self.url = reverse("pass_turn", args=[self.match.pk])

    def test_pass_turn_black_to_white(self):
        response = self.client.post(self.url)
        self.match.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.match.turn, "white's turn")
        self.assertEqual(response.json()["message"], "Player passed.")
        self.assertEqual(response.json()["turn"], "white's turn")

    def test_pass_turn_white_to_black(self):
        self.match.turn = "white's turn"
        self.match.save()
        response = self.client.post(self.url)
        self.match.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.match.turn, "black's turn")
        self.assertEqual(response.json()["message"], "Player passed.")
        self.assertEqual(response.json()["turn"], "black's turn")


class EndGameViewViewTest(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )
        self.url = reverse("end_game", args=[self.match.pk])

    @patch("apps.othello.views.end_game")
    def test_end_game_black_wins(self, mock_end_game):
        # モックの設定
        mock_end_game.return_value = {
            "blackCount": 40,
            "whiteCount": 24,
            "winner": "black",
        }

        response = self.client.post(self.url)
        self.match.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.match.result, "black")
        self.assertEqual(response.json()["blackCount"], 40)
        self.assertEqual(response.json()["whiteCount"], 24)
        self.assertEqual(response.json()["winner"], "black")
        # end_game関数が正しい引数で呼ばれたことを確認
        mock_end_game.assert_called_once_with(self.match.board)

    @patch("apps.othello.views.end_game")
    def test_end_game_draw(self, mock_end_game):
        mock_end_game.return_value = {
            "blackCount": 32,
            "whiteCount": 32,
            "winner": "draw",
        }

        # ボードをセット（例えば、駒の数が同じ場合など）
        self.match.board = [["black"] * 4 + ["white"] * 4] * 8  # 偽のボードデータ
        self.match.save()

        response = self.client.post(self.url)
        self.match.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.match.result, "draw")
        self.assertEqual(response.json()["blackCount"], 32)
        self.assertEqual(response.json()["whiteCount"], 32)
        self.assertEqual(response.json()["winner"], "draw")
