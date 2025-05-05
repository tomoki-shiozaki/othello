# このファイルは、URLの解決およびビューの正常なアクセス（所有者によるアクセス）を確認するためのテストを集めています。
# アクセス制御（未ログイン・他人アクセス）は test_permissions.py を参照。

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from othello.models import AuthenticatedLocalMatch


class TestOwnerLoginMixin:
    def login_user(self, username="testuser", password="testpassword"):
        user = get_user_model().objects.create_user(
            username=username, password=password
        )
        self.client.login(username=username, password=password)
        return user


class TestAuthenticatedLocalMatchAccess(TestOwnerLoginMixin, TestCase):
    def setUp(self):
        self.user = self.login_user()
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )

    def test_list_url_access(self):
        response = self.client.get(reverse("local_match_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aliceさん")

    def test_owner_can_access_new_view(self):
        response = self.client.get(reverse("local_match_new"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "新しい対局")

    def test_owner_can_access_delete_view(self):
        response = self.client.get(reverse("local_match_delete", args=[self.match.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "削除")

    def test_owner_can_access_play_view(self):
        response = self.client.get(reverse("local_match_play", args=[self.match.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
