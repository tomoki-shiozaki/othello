import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Game
from .logic import Rule


# Create your views here.
def place_piece_view(request):
    if request.method == "POST":
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get("cell", 10000)

            # 最新のゲームオブジェクトを取得
            game = Game.objects.last()
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
    return JsonResponse({"error": "Invalid request method"}, status=400)


def local_match(request):

    # game = Game.objects.first()
    # 最新のゲームオブジェクトを取得
    game = Game.objects.last()

    return render(
        request,
        "match/local.html",
        {
            "game": game,
            "turn": game.turn,
            "board": json.dumps(game.board),  # board を JSON 形式に変換して渡す
            #'board': json.dumps(game.board)  # board を JSON 形式に変換して渡す
        },
    )


def start_new_game(request):

    # ゲームオブジェクトを作成
    Game.objects.create()
    # 新しいゲームが作成されたら、ホームページ（ゲーム進行ページ）にリダイレクト
    return redirect("/")


def pass_turn(request):
    if request.method == "POST":
        try:
            # 最新のゲームオブジェクトを取得
            game = Game.objects.last()
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
