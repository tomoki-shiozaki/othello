from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.guest_games.forms import GuestGameCreationForm
from apps.guest_games.utils import default_board


# Create your views here.
class GuestGameHomeView(TemplateView):
    template_name = "guest_games/guest_game_home.html"


class GuestGameStartView(FormView):
    template_name = "guest_games/guest_game_new.html"
    form_class = GuestGameCreationForm
    success_url = reverse_lazy("guest_games:play")  # ゲームプレイ画面へリダイレクト

    def form_valid(self, form):
        # フォームが有効な場合の処理
        self.request.session["guest_game"] = {
            "black_player": form.cleaned_data["black_player"],
            "white_player": form.cleaned_data["white_player"],
            "turn": "black's turn",
            "board": default_board(),
            "result": "対局中",
        }
        # 続けてsuperでsuccess_urlにリダイレクト
        return super().form_valid(form)


def guest_play_view(request):
    game = request.session.get("guest_game")
    if not game:
        return redirect("guest_games:new")

    return render(request, "guest_games/guest_game_play.html", {"game": game})
