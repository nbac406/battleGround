from django.shortcuts import render, redirect
import requests
import json
from config.settings.prod import API_KEY
from .models import players, match_summary, weapon_mastery, match_participant, logs
from django.db import transaction

# Create your views here.

def index(request):
    return render(request, 'main.html')

@transaction.atomic
def profile(request):
    user = request.POST.get("user_name")
    context = {'user_name' : user}
    user_url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={user}'
    headers = {'Authorization': API_KEY,
               "Accept": "application/vnd.api+json"}

    try:
        player_response = requests.get(user_url, headers=headers)
        player_response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        player_data_json = player_response.json()
        player_data_list = player_data_json['data'][0]
        account_id = player_data_list['id']
        user_name = player_data_list['attributes']['name']
        user_server = player_data_list['attributes']['shardId']
        match_history = player_data_list['relationships']['matches']['data']

        data = {
            'account_id' : account_id,
            'user_name' : user_name,
            'user_server' : user_server,
            'match_history' : match_history
        }

        url2 = f"https://api.pubg.com/shards/kakao/players/{account_id}/weapon_mastery"
        weapon_mastery_response = requests.get(url2, headers=headers)
        
        if weapon_mastery_response.status_code == 200:
            weapon_mastery_data_json = weapon_mastery_response.json()
            weapon_mastery_data_list = weapon_mastery_data_json['data']['attributes']['weaponSummaries']
            
            # 경험치를 기준으로 무기 정렬
            sorted_weapons = sorted(weapon_mastery_data_list.items(), key=lambda x: x[1]['XPTotal'], reverse=True)
            
            # 상위 3개 무기 출력
            top3_weapons = sorted_weapons[:3]
            
            for idx, weapon in enumerate(top3_weapons, start=1):
                weapon_name = weapon[0].split('_')[-2] # Split the string to get the weapon name
                experience = weapon[1]['XPTotal']

                print(f"Top {idx}: {weapon_name} - 경험치: {experience}")

                w_mastery = weapon_mastery(
                    accountId = account_id,
                    Item_Weapon_name = weapon_name,
                    Item_Weapon_XPtotal = experience
                )

                w_mastery.save()

        matchIds = []
        for i in range(len(match_history)):
            matchIds.append(match_history[i].get('id'))

        for i in matchIds: 
            match_url = f"https://api.pubg.com/shards/steam/matches/{i}" 
            match_response = requests.get(match_url, headers=headers)
            match_response.raise_for_status()
            
            if match_response.status_code == 200 : 
                match_data_json = match_response.json()

                for j in range(len(match_data_json['included'])) :
                    
                    # player 테이블 저장
                    if j == 0:
                        createAt = match_data_json['data']['attributes']['createdAt']
                        p = players(
                            accountId=account_id, player_name=user_name, shardid=user_server, matchId=i, created_at=createAt)
                        p.save()

                    # match_summary 테이블 저장
                    if match_data_json['included'][j]['type'] == 'asset':
                        createAt = match_data_json['data']['attributes']['createdAt']
                        gameMode = match_data_json['data']['attributes']['gameMode']
                        mapname = match_data_json['data']['attributes']['mapName']
                        duration = match_data_json['data']['attributes']['duration']
                        match_type = match_data_json['data']['attributes']['matchType']
                        asset_url = match_data_json['included'][j]['attributes']['URL']
 
                        m_summary = match_summary(
                            matchId = i,
                            createdAt = createAt,
                            gamemode = gameMode, 
                            mapname = mapname,
                            duration = duration, 
                            match_type = match_type, 
                            asset_url = asset_url                            
                        )
                        
                        m_summary.save()           
            

                    elif match_data_json['included'][j]['type'] == 'participant':
                        player_name = match_data_json['included'][j]['attributes']['stats']['name']
                        accountId = match_data_json['included'][j]['attributes']['stats']['playerId']
                        team_ranking = match_data_json['included'][j]['attributes']['stats']['winPlace']
                        DBNOs = match_data_json['included'][j]['attributes']['stats']['DBNOs']
                        assists = match_data_json['included'][j]['attributes']['stats']['assists']
                        damageDealt = match_data_json['included'][j]['attributes']['stats']['damageDealt']
                        headshotkills = match_data_json['included'][j]['attributes']['stats']['headshotKills']
                        kills = match_data_json['included'][j]['attributes']['stats']['kills']
                        longestkill = match_data_json['included'][j]['attributes']['stats']['longestKill']
                        teamkills = match_data_json['included'][j]['attributes']['stats']['teamKills']
                        rideDistance = match_data_json['included'][j]['attributes']['stats']['rideDistance']
                        swimDistance = match_data_json['included'][j]['attributes']['stats']['swimDistance']
                        walkDistance = match_data_json['included'][j]['attributes']['stats']['walkDistance']
            
                        m_participant = match_participant(
                            matchId = i,
                            player_name = player_name,
                            accountId = accountId,
                            team_ranking = team_ranking,
                            dbnos = DBNOs,
                            assists = assists,
                            damage_dealt = damageDealt,
                            headshot_kills = headshotkills,
                            kills = kills,
                            longestkill = longestkill,
                            team_kills = teamkills,
                            ride_distance = rideDistance,
                            swim_distance = swimDistance,
                            walk_distance = walkDistance
                        )
                        
                        m_participant.save()
            
        
            

        return render(request, 'profile.html', data)
    
    except requests.exceptions.RequestException as e:
        print('API 요청 오류:', e)
        return render(request, 'main.html')
    
