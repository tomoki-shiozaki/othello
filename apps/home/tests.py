from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


# Create your tests here.
class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(
            response.status_code, 200
        )  # ステータスコードが200であることを確認

    def test_view_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class TopPageViewTests(TestCase):
    def setUp(self):
        self.url = reverse("home")

    def test_top_page_for_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertContains(
            response, "アカウント登録で、対局データの保存や履歴確認が可能になります"
        )
        self.assertContains(response, f'href="{reverse("login")}"')
        self.assertContains(response, f'href="{reverse("signup")}"')
        self.assertContains(response, f'href="{reverse("guest_games:home")}"')

    def test_top_page_for_login_user(self):
        user = get_user_model().objects.create_user(
            username="user",
            email="user@example.com",
            password="testpass",
        )
        self.client.login(username="user", password="testpass")
        response = self.client.get(self.url)
        self.assertContains(response, "ようこそ")
        self.assertContains(response, f'href="{reverse("local_match_list")}"')
        self.assertContains(response, f'href="{reverse("local_match_new")}"')
