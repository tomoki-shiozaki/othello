from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from othello.models import AuthenticatedLocalMatch
from othello.views import AuthenticatedLocalMatchListView


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
