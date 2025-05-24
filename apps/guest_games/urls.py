from django.urls import path

from apps.guest_games.views import (
    GuestGameTopView,
    GuestGameCreationFormView,
)
from django.views.generic import TemplateView

app_name = "guest_games"

urlpatterns = [
    path("", GuestGameTopView.as_view(), name="home"),
    path("new/", GuestGameCreationFormView.as_view(), name="new"),
    path(
        "play/",
        TemplateView.as_view(template_name="guest_games/guest_game_play.html"),
        name="play",
    ),
]
