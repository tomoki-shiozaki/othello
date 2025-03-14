from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt  # CSRFトークンを無効化（開発中のみ使用、実際のプロダクションでは適切に対策が必要）
def fetch_data(request):
    if request.method == "POST":
        try:
            # リクエストボディをJSONとしてパース
            body = json.loads(request.body)
            turn = body.get('turn', 'Unknown')
            cell = body.get('cell', 10000)

            # レスポンスデータの作成
            response_data = {
                'message': f'It\'s {turn}\'s turn! You put the piece in the {cell} cell.',
                'received': body
            }

            return JsonResponse(response_data)
    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def home(request):
    return render(request, 'home.html')