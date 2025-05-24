from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from apps.guest_games.forms import GuestGameCreationForm


# Create your views here.
class GuestGameTopView(TemplateView):
    template_name = "guest_games/guest_game_home.html"


class GuestGameCreationFormView(FormView):
    template_name = "guest_games/guest_game_new.html"  # フォームのテンプレート
    form_class = GuestGameCreationForm  # 使用するフォームクラス
    success_url = reverse_lazy("guest_games:play")  # 成功時リダイレクト先

    def form_valid(self, form):
        # フォームが有効な場合の処理
        # 例えばメール送信やセッション保存などをここで実施

        # 例：セッションに名前を保存
        self.request.session["black_player"] = form.cleaned_data["black_player"]
        self.request.session["white_player"] = form.cleaned_data["white_player"]

        # 続けてsuperでsuccess_urlにリダイレクト
        return super().form_valid(form)
