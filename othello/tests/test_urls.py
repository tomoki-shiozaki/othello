from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AuthenticatedLocalMatchListUrlTest(TestCase):
    def test_url_resolves_to_view(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        # ログイン処理
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get("/match/local/")
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_view_by_name(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        # ログイン処理
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(reverse("local_match_list"))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("local_match_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/accounts/login/?next={reverse('local_match_list')}"
        )
