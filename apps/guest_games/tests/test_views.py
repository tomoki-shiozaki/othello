# from django.test import TestCase, RequestFactory
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# import json
# from unittest.mock import patch
# import logging

# from ..models import AuthenticatedLocalMatch
# from ..views import AuthenticatedLocalMatchListView


# class TestGuestGameCreateView(TestOwnerLoginMixin, TestCase):
#     def setUp(self):
#         self.user = self.login_user()
#         self.create_url = reverse("local_match_new")

#     def test_create_match_success(self):
#         response = self.client.post(
#             self.create_url,
#             {
#                 "black_player": "Alice",
#                 "white_player": "Bob",
#             },
#         )

#         # リダイレクトされているか（CreateViewの成功時）
#         self.assertEqual(response.status_code, 302)

#         # 作成されたオブジェクトを確認
#         match = AuthenticatedLocalMatch.objects.first()
#         self.assertIsNotNone(match)
#         self.assertEqual(match.black_player, "Alice")
#         self.assertEqual(match.white_player, "Bob")
#         self.assertEqual(match.authenticated_user, self.user)

#     def test_uses_correct_template(self):
#         response = self.client.get(self.create_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "match/local/new.html")

#     def test_invalid_form(self):
#         # 空フォーム送信（black_player, white_playerともに入力必須。バリデーションエラーが起こる）
#         response = self.client.post(self.create_url, {})
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(
#             response.context["form"], "black_player", "このフィールドは必須です。"
#         )
#         self.assertFormError(
#             response.context["form"], "white_player", "このフィールドは必須です。"
#         )
