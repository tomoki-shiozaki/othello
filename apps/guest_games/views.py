from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class GuestGameTopView(TemplateView):
    template_name = "guest_games/guest_game_home.html"
