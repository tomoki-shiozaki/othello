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
class AuthenticatedLocalMatchListView(LoginRequiredMixin, ListView):
    model = AuthenticatedLocalMatch
    template_name = "match/local/list.html"

    def get_queryset(self):
        return AuthenticatedLocalMatch.objects.filter(
            authenticated_user=self.request.user
        )


class AuthenticatedLocalMatchPermissionMixin:
    def get_object(self):
        obj = get_object_or_404(AuthenticatedLocalMatch, pk=self.kwargs["pk"])
        if obj.authenticated_user != self.request.user:
            raise PermissionDenied("このゲームにアクセスする権限がありません。")
        return obj


class AuthenticatedLocalMatchPlayView(
    LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, View
):
    def get(self, request, pk):
        match = self.get_object()
        # try:
        #     # pk に基づいてゲームを取得
        #     game = AuthenticatedLocalMatch.objects.get(
        #         pk=pk, authenticated_user=self.request.user
        #     )
        # except AuthenticatedLocalMatch.DoesNotExist:
        #     return render(request, "match/error.html", {"error": "Game not found"})

        return render(
            request,
            "match/local.html",
            {
                "match": match,
                "board": json.dumps(match.board),
            },
        )


class AuthenticatedLocalMatchDeleteView(
    LoginRequiredMixin, AuthenticatedLocalMatchPermissionMixin, DeleteView
):
    model = AuthenticatedLocalMatch
    template_name = "match/local/delete.html"
    success_url = reverse_lazy("local_match_list")


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


# class ArticleDetailView(DetailView):
#     model = AuthenticatedLocalMatch
#     template_name = "match/local/detail.html"


# class ArticleUpdateView(UpdateView):  # new
#     model = Article
#     fields = (
#         "title",
#         "body",
#     )
#     template_name = "article_edit.html"


class AuthenticatedLocalMatchPlacePieceView(View):
    def post(self, request):

        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get("cell", 10000)
            pk = body.get("pk")
            game = AuthenticatedLocalMatch.objects.get(
                pk=pk, authenticated_user=self.request.user
            )
            board = game.board
            turn = game.turn

            # ゲームの進行処理
            rule = Rule(
                board, cell, turn
            )  # Ruleクラスは、ゲームのルールを記述したクラス
            if (
                rule.can_place_piece()
            ):  # can_place_piece()メソッドは、駒をおけるときにTrue
                rule.place_piece()  # 駒を打って、盤面を書き換える
                rule.change_turn()

                # ゲームの盤面とターンを変更
                game.board = rule.board
                game.turn = rule.turn

                # 変更を保存
                game.save()

                # レスポンスデータの作成
            response_data = {
                "message": f"It's {game.turn}! You put the piece in the {cell} cell.",
                "received": body,
                "board": game.board,
                "turn": game.turn,
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


# def place_piece_view(request):
#     if request.method == "POST":
#         try:
#             # リクエストボディをJSONとしてパース
#             body = json.loads(request.body)
#             cell = body.get("cell", 10000)

#             # 最新のゲームオブジェクトを取得
#             game = AuthenticatedLocalMatch.objects.last()
#             board = game.board
#             turn = game.turn

#             # ゲームの進行処理
#             rule = Rule(
#                 board, cell, turn
#             )  # Ruleクラスは、ゲームのルールを記述したクラス
#             if (
#                 rule.can_place_piece()
#             ):  # can_place_piece()メソッドは、駒をおけるときにTrue
#                 rule.place_piece()  # 駒を打って、盤面を書き換える
#                 rule.change_turn()

#                 # ゲームの盤面とターンを変更
#                 game.board = rule.board
#                 game.turn = rule.turn

#                 # 変更を保存
#                 game.save()

#             # レスポンスデータの作成
#             response_data = {
#                 "message": f"It's {game.turn}! You put the piece in the {cell} cell.",
#                 "received": body,
#                 "board": game.board,
#                 "turn": game.turn,
#             }

#             return JsonResponse(response_data)

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=400)


# def local_match(request):

#     # game = Game.objects.first()
#     # 最新のゲームオブジェクトを取得
#     game = AuthenticatedLocalMatch.objects.last()

#     return render(
#         request,
#         "match/local.html",
#         {
#             "game": game,
#             "turn": game.turn,
#             "board": json.dumps(game.board),  # board を JSON 形式に変換して渡す
#             #'board': json.dumps(game.board)  # board を JSON 形式に変換して渡す
#         },
#     )


def start_new_game(request):

    # ゲームオブジェクトを作成
    AuthenticatedLocalMatch.objects.create()
    # 新しいゲームが作成されたら、ホームページ（ゲーム進行ページ）にリダイレクト
    return redirect("/")


def pass_turn(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            pk = body.get("pk")
            game = AuthenticatedLocalMatch.objects.get(
                pk=pk, authenticated_user=request.user
            )
            # 最新のゲームオブジェクトを取得
            # game = AuthenticatedLocalMatch.objects.last()
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
            # 対局結果を格納する
            game.result = results["winner"]
            # 変更を保存
            game.save()

            return JsonResponse(results)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)
