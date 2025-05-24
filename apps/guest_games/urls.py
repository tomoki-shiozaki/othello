from django.urls import path

from apps.guest_games.views import GuestGameTopView

app_name = "guest_games"

urlpatterns = [
    path("", GuestGameTopView.as_view(), name="home"),
]
