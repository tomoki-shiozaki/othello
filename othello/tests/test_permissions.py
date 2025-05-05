from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from othello.models import AuthenticatedLocalMatch
from othello.views import AuthenticatedLocalMatchPermissionMixin


class TestAuthenticatedLocalMatchPermissionMixin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(
            username="testuser", password="testpass", email="testuser@email.com"
        )
        self.other_user = get_user_model().objects.create(
            username="testuser2", password="testpass2", email="testuser2@email.com"
        )
        self.game = AuthenticatedLocalMatch.objects.create(authenticated_user=self.user)

    def test_get_object_success(self):
        class TestView(AuthenticatedLocalMatchPermissionMixin):
            def __init__(self, request, kwargs):
                self.request = request
                self.kwargs = kwargs

        request = self.factory.get("/")
        request.user = self.user
        view = TestView(request, {"pk": self.game.pk})
        obj = view.get_object()
        self.assertEqual(obj, self.game)

    def test_get_object_permission_denied(self):
        class TestView(AuthenticatedLocalMatchPermissionMixin):
            def __init__(self, request, kwargs):
                self.request = request
                self.kwargs = kwargs

        request = self.factory.get("/")
        request.user = self.other_user
        view = TestView(request, {"pk": self.game.pk})
        with self.assertRaises(PermissionDenied):
            view.get_object()


class LoginRequiredTestMixin:
    login_required_urls = []  # [reverse("url_name", args=[pk]) or just URL strings]

    def test_login_required_redirects(self):
        for url in self.login_required_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))
            self.assertRedirects(response, f"/accounts/login/?next={url}")


class PermissionDeniedTestMixin:
    permission_protected_urls = []  # list of (url_func, kwargs)

    def test_permission_denied_for_other_user(self):
        other_user = get_user_model().objects.create_user(
            username="other", password="passother"
        )
        self.client.force_login(other_user)

        for url_func, kwargs in self.permission_protected_urls:
            response = url_func(self.client, **kwargs)
            self.assertEqual(response.status_code, 403)


# --- アクセス制御の結合テスト ---
# AuthenticatedLocalMatch-List, Create, Delete, Play-Viewのパーミッションをテスト
class TestAuthenticatedLocalMatchAccessControl(
    LoginRequiredTestMixin, PermissionDeniedTestMixin, TestCase
):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user", password="pass"
        )
        self.match = AuthenticatedLocalMatch.objects.create(
            authenticated_user=self.user,
            black_player="Alice",
            white_player="Bob",
        )

        self.login_required_urls = [
            reverse("local_match_list"),
            reverse("local_match_play", args=[self.match.pk]),
            reverse("local_match_delete", args=[self.match.pk]),
        ]

        self.permission_protected_urls = [
            (
                lambda client, **kwargs: client.get(
                    reverse("local_match_play", args=[kwargs["pk"]])
                ),
                {"pk": self.match.pk},
            ),
            (
                lambda client, **kwargs: client.post(
                    reverse("local_match_delete", args=[kwargs["pk"]])
                ),
                {"pk": self.match.pk},
            ),
        ]
