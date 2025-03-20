import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Game
from .logic import Rule

# Create your views here.
@csrf_exempt  # CSRFトークンを無効化（開発中のみ使用、実際のプロダクションでは適切に対策が必要）
def fetch_data(request):
    if request.method == "POST":
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            cell = body.get('cell', 10000)

            #ゲームオブジェクトを取得
            game = Game.objects.first()
            board = game.board
            turn = game.turn

            #ゲームの進行処理
            rule = Rule(board, cell, turn) #Ruleクラスは、ゲームのルールを記述したクラス
            if rule.can_place_piece(): #can_place_piece()メソッドは、駒をおけるときにTrue
                rule.place_piece() #駒を打って、盤面を書き換える
                rule.change_turn()
            
                #ゲームの盤面とターンを変更
                game.board = rule.board
                game.turn  = rule.turn

                #変更を保存
                game.save()
            
            # レスポンスデータの作成
            response_data = {
                'message': f'It\'s {game.turn}! You put the piece in the {cell} cell.',
                'received': body,
                'board': game.board,
            }

            return JsonResponse(response_data)
    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def home(request):

    game = Game.objects.first()
    
    return render(request, 'home.html', {
        'game': game,
        'turn': game.turn,
        'board': json.dumps(game.board)  # board を JSON 形式に変換して渡す
        #'board': json.dumps(game.board)  # board を JSON 形式に変換して渡す
    })

def start_new_game(request):
    Game.objects.all().delete()
    #盤面の初期状態を定義
    initial_board=[]
    for _ in range(8):
        initial_board.append(['empty']*8)
    initial_board[3][3] = 'black'
    initial_board[4][4] = 'black'
    initial_board[3][4] = 'white'
    initial_board[4][3] = 'white'

    # ゲームオブジェクトを作成し、初期盤面やターンを設定
    Game.objects.create(board=initial_board, turn='black\'s turn')
    # 新しいゲームが作成されたら、ホームページ（ゲーム進行ページ）にリダイレクト
    return redirect('/')

@csrf_exempt
def pass_turn(request):
    if request.method == "POST":
        try:
            #ゲームオブジェクトを取得
            game = Game.objects.first()            
            if game.turn == 'black\'s turn':
                game.turn = 'white\'s turn'
            else:
                game.turn = 'black\'s turn'                  

            #変更を保存
            game.save()
            
            # レスポンスデータの作成
            response_data = {
                'message': 'Player passed.'
            }

            return JsonResponse(response_data)
    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
