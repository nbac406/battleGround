from django.shortcuts import render, redirect
import requests

# Create your views here.

def index(request):
    return render(request, 'main.html')

def profile(request):
    user = request.POST.get("user_name")
    context = {'user_name' : user}
    url = f'https://api.battlegroundsgame.com/shards/steam/players?filter[playerNames]={user}'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()
        player_info = data['data'][0]  # 첫 번째 플레이어 정보 가져오기
        print(player_info)
        return player_info
    
    except requests.exceptions.RequestException as e:
        print('API 요청 오류:', e)
        return None
    
    return render(request, 'profile.html', context)