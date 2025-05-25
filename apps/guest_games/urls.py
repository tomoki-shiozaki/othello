from django.urls import path

from apps.guest_games.views import (
    GuestGameHomeView,
    GuestGameStartView,
)
from apps.guest_games.views import guest_play_view
from django.views.generic import TemplateView

app_name = "guest_games"

urlpatterns = [
    path("", GuestGameHomeView.as_view(), name="home"),
    path("new/", GuestGameStartView.as_view(), name="new"),
    # path(
    #     "play/",
    #     TemplateView.as_view(template_name="guest_games/guest_game_play.html"),
    #     name="play",
    # ),
    path("play/", guest_play_view, name="play"),
]
