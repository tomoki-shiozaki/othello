import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404

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


class AuthenticatedLocalMatchCreateView(LoginRequiredMixin, CreateView):
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


logger = logging.getLogger(__name__)


class AuthenticatedLocalMatchPlacePieceView(
    LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, View
):
    def post(self, request, pk):
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get("cell")
            # 0〜63 の整数かどうかを検証
            if not isinstance(cell, int) or not (0 <= cell <= 63):
                return JsonResponse({"error": "Invalid cell value"}, status=400)

            game = self.get_object()
            board = game.board
            turn = game.turn

            # ゲームのロジック処理を行う
            # Ruleクラスはゲームのルールを記述したクラス
            rule = Rule(board, cell, turn)
            # 駒を置けるかどうかの結果を取得する
            placement_result = rule.find_reversable_pieces()
            can_place_piece = placement_result["can_place_piece"]
            reversable_pieces = placement_result["reversable_pieces"]
            # 駒をおける場合、駒を置いて、相手の駒をひっくり返し、ターンを進める
            if can_place_piece:
                rule.place_and_reverse_pieces(reversable_pieces)
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
        except PermissionDenied:
            return JsonResponse({"error": "Permission denied"}, status=403)
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)
        except Exception as e:
            logger.exception(
                f"Unexpected error in AuthenticatedLocalMatchPlacePieceView: {str(e)}"
            )
            return JsonResponse({"error": "Internal server error"}, status=500)


class PassTurnView(LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, View):
    def post(self, request, pk):
        game = self.get_object()  # mixinでチェック済み

        # ターン切り替え
        game.turn = "white's turn" if game.turn == "black's turn" else "black's turn"
        game.save()

        return JsonResponse(
            {
                "message": "Player passed.",
                "turn": game.turn,
            }
        )


class EndGameView(LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, View):
    def post(self, request, pk):
        game = self.get_object()  # mixinでチェック済み

        results = end_game(game.board)
        # 対局結果をデータベースに格納する
        game.result = results["winner"]
        # 変更を保存
        game.save()

        return JsonResponse(results)
