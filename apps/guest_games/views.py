import json
import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404

from apps.guest_games.forms import GuestGameCreationForm
from apps.guest_games.utils import default_board, Rule, end_game


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


logger = logging.getLogger(__name__)


class GuestGamePlacePieceView(View):
    def post(self, request):
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get("cell")
            # 0〜63 の整数かどうかを検証
            if not isinstance(cell, int) or not (0 <= cell <= 63):
                return JsonResponse({"error": "Invalid cell value"}, status=400)

            game = request.session.get("guest_game")
            board = game["board"]
            turn = game["turn"]

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
                game["board"] = rule.board
                game["turn"] = rule.turn

                # 変更を保存
                request.session["guest_game"] = game

            return JsonResponse(
                {
                    "board": game["board"],
                    "turn": game["turn"],
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except PermissionDenied:
            return JsonResponse({"error": "Permission denied"}, status=403)
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)
        except Exception as e:
            logger.exception(f"Unexpected error in GuestGamePlacePieceView: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)


class PassTurnView(View):
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


class EndGameView(View):
    def post(self, request, pk):
        game = self.get_object()  # mixinでチェック済み

        results = end_game(game.board)
        # 対局結果をデータベースに格納する
        game.result = results["winner"]
        # 変更を保存
        game.save()

        return JsonResponse(results)
