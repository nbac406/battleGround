from django.shortcuts import render, redirect
import requests
import json
from config.settings.prod import API_KEY

# Create your views here.

def index(request):
    return render(request, 'main.html')

def profile(request):
    user = request.POST.get("user_name")
    context = {'user_name' : user}
    url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={user}'
    headers = {'Authorization': API_KEY,
               "Accept": "application/vnd.api+json"}

    try:
        response = requests.get(url, headers=headers)
        print(response)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data_json = response.json()
        data_list = data_json['data'][0]
        account_id = data_list['id']
        user_name = data_list['attributes']['name']
        user_server = data_list['attributes']['shardId']
        match_history = data_list['relationships']['matches']['data']

        data = {
            'account_id' : account_id,
            'user_name' : user_name,
            'user_server' : user_server,
            'match_history' : match_history
        }
        matchId = {}
        for i in range(len(match_history)):
            matchId[i+1] = match_history[i].get('id')
        return render(request, 'profile.html', data)
    
    except requests.exceptions.RequestException as e:
        print('API 요청 오류:', e)
        return render(request, 'main.html')
    
