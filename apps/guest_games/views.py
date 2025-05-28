import json
import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse
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


class GuestGameSessionMixin:
    def get_guest_game(self, request):
        game = request.session.get("guest_game")
        if game is None:
            raise Http404("Game session not found")

        if not isinstance(game, dict):
            raise ValueError("Game session is corrupted (invalid format)")

        # boardが8行で、各行が8要素のリストかどうかを確認
        board = game.get("board")
        if not (isinstance(board, list) and len(board) == 8):
            raise ValueError("Invalid board data: must have 8 rows")
        for row in board:
            if not (isinstance(row, list) and len(row) == 8):
                raise ValueError("Invalid board data: each row must have 8 columns")

        # 盤面の要素の型チェック（全てstrか）と検証
        valid_cells = {"black", "white", "empty"}
        for row in board:
            for cell in row:
                # 駒の状態が文字列かどうか
                if not isinstance(cell, str):
                    raise ValueError("Invalid board cell data: must be string")
                if cell not in valid_cells:
                    raise ValueError(
                        f"Invalid board cell value: {cell} (must be one of {valid_cells})"
                    )

        # turnの検証
        if game.get("turn") not in ("black's turn", "white's turn"):
            raise ValueError("Invalid turn data")

        # player名の検証（文字列か）
        if not all(
            isinstance(game.get(k), str) for k in ("black_player", "white_player")
        ):
            raise ValueError("Invalid player data")

        # resultの検証（想定値）
        valid_results = {"対局中", "black", "white", "draw"}
        if game.get("result") not in valid_results:
            raise ValueError("Invalid game result")

        return game


def guest_play_view(request):
    game = request.session.get("guest_game")
    if not game:
        return redirect("guest_games:new")

    return render(request, "guest_games/guest_game_play.html", {"game": game})


class GuestGamePlayView(GuestGameSessionMixin, TemplateView):
    template_name = "guest_games/guest_game_play.html"

    def get(self, request, *args, **kwargs):
        try:
            game = self.get_guest_game(request)
        except (Http404, ValueError):
            return redirect("guest_games:new")
        return self.render_to_response({"game": game})


logger = logging.getLogger(__name__)


class GuestGamePlacePieceView(GuestGameSessionMixin, View):
    def post(self, request):
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get("cell")
            # 0〜63 の整数かどうかを検証
            if not isinstance(cell, int) or not (0 <= cell <= 63):
                return JsonResponse({"error": "Invalid cell value"}, status=400)

            game = self.get_guest_game(request)
            board = game["board"]
            turn = game["turn"]

            if game.get("result") != "対局中":
                return JsonResponse({"error": "Game has already ended."}, status=400)

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
        except Http404:
            return JsonResponse({"error": "Game session not found"}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.exception(f"Unexpected error in GuestGamePlacePieceView: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)


class GuestGamePassTurnView(GuestGameSessionMixin, View):
    def post(self, request):
        try:
            game = self.get_guest_game(request)

            if game.get("result") != "対局中":
                return JsonResponse({"error": "Game has already ended."}, status=400)

            # ターン切り替え
            game["turn"] = (
                "white's turn" if game["turn"] == "black's turn" else "black's turn"
            )
            request.session["guest_game"] = game

            return JsonResponse(
                {
                    "message": "Player passed.",
                    "turn": game["turn"],
                }
            )

        except Http404:
            return JsonResponse({"error": "Game session not found"}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.exception(f"Unexpected error in GuestGamePassTurnView: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)


class GuestGameEndView(GuestGameSessionMixin, View):
    def post(self, request):
        try:
            game = self.get_guest_game(request)

            results = end_game(game["board"])
            game["result"] = results["winner"]
            request.session["guest_game"] = game

            return JsonResponse(results)

        except Http404:
            return JsonResponse({"error": "Game session not found"}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.exception(f"Unexpected error in GuestGameEndView: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)
