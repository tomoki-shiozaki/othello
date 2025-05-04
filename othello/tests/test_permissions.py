from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

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
