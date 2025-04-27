import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import AuthenticatedLocalMatch
from .logic import Rule, end_game


# Create your views here.
class AuthenticatedLocalMatchPermissionMixin:
    def get_object(self):
        obj = get_object_or_404(AuthenticatedLocalMatch, pk=self.kwargs["pk"])
        if obj.authenticated_user != self.request.user:
            raise PermissionDenied
        return obj


class AuthenticatedLocalMatchListView(LoginRequiredMixin, ListView):
    model = AuthenticatedLocalMatch
    template_name = "match/local/list.html"

    def get_queryset(self):
        return AuthenticatedLocalMatch.objects.filter(
            authenticated_user=self.request.user
        )


class AuthenticatedLocalMatchCreateView(
    LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, CreateView
):
    model = AuthenticatedLocalMatch
    template_name = "match/local/new.html"
    fields = (
        "black_player",
        "white_player",
    )

    def form_valid(self, form):  # new
        form.instance.authenticated_user = self.request.user
        return super().form_valid(form)


class AuthenticatedLocalMatchDeleteView(
    LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, DeleteView
):
    model = AuthenticatedLocalMatch
    template_name = "match/local/delete.html"
    success_url = reverse_lazy("local_match_list")


class AuthenticatedLocalMatchPlayView(
    LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, View
):
    def get(self, request, pk):
        match = self.get_object()

        return render(
            request,
            "match/local.html",
            {
                "match": match,
                "board": json.dumps(match.board),
            },
        )


class AuthenticatedLocalMatchPlacePieceView(View):
    def post(self, request):
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get("cell")
            pk = body.get("pk")
            game = AuthenticatedLocalMatch.objects.get(
                pk=pk, authenticated_user=self.request.user
            )
            board = game.board
            turn = game.turn

            # ゲームのロジック処理を行う
            # Ruleクラスはゲームのルールを記述したクラス
            rule = Rule(board, cell, turn)
            # can_place_piece()メソッドは、駒をおけるときにTrue
            if rule.can_place_piece():
                rule.place_piece()  # 駒を打って、盤面を書き換える
                rule.change_turn()

                # ゲームの盤面とターンを変更
                game.board = rule.board
                game.turn = rule.turn

                # 変更を保存
                game.save()

                # レスポンスデータの作成
            response_data = {
                "board": game.board,
                "turn": game.turn,
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


def pass_turn(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            pk = body.get("pk")
            game = AuthenticatedLocalMatch.objects.get(
                pk=pk, authenticated_user=request.user
            )
            if game.turn == "black's turn":
                game.turn = "white's turn"
            else:
                game.turn = "black's turn"

            # 変更を保存
            game.save()

            # レスポンスデータの作成
            response_data = {
                "message": "Player passed.",
                "turn": game.turn,
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def end_game_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            pk = body.get("pk")
            game = AuthenticatedLocalMatch.objects.get(
                pk=pk, authenticated_user=request.user
            )
            results = end_game(game.board)
            # 対局結果をデータベースに格納する
            game.result = results["winner"]
            # 変更を保存
            game.save()

            return JsonResponse(results)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)
