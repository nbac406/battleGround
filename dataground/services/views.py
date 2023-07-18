from django.shortcuts import render, redirect
import requests
from config.settings.prod import KEY
from .models import players, match_summarys, weapon_masterys, match_participants, position_logs, kill_logs, weapons, weapon_parts
from django.db import transaction, IntegrityError
from datetime import datetime, timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import pandas as pd

def index(request):
    return render(request, 'main.html')

def profile(request):
    print(request.method)
    if request.method == 'GET':
        service = request.GET.get("service")
        user_name = request.GET.get("user_name")
        
        current_date = datetime.now()
        past_date = current_date - timedelta(days=30)
        players.objects.filter(created_at__lt=past_date).delete()
        
        user_data = players.objects.filter(player_name=user_name)
        user_data_match_ids = user_data.values_list('match_id', flat=True)
        
        match_participant_data = []
        
        for match_id in user_data_match_ids:
            m_data = {
                'match_participant_data': match_participants.objects.filter(match_id=match_id, player_name=user_name),
                'game_mode' : match_summarys.objects.filter(match_id=match_id).values('game_mode'),
                'created_at': players.objects.filter(match_id=match_id, player_name=user_name).values('created_at').first(),
            }
            match_participant_data.append(m_data)
        
        data = {
            'user_name': user_name,
            'user_service': service,
            'match_participant_data': match_participant_data,
        }

        return render(request, 'profile.html', data)

    return redirect('services:index')

def profile_update(request):
    service = request.POST.get("service")
    user = request.POST.get("user_name")
    user_url = f'https://api.pubg.com/shards/{service}/players?filter[playerNames]={user}'
    headers = {'Authorization': KEY[0],
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


        matchIds = []
        for i in range(len(match_history)):
            matchIds.append(match_history[i].get('id'))

        for idx, i in enumerate(matchIds):
            headers = {'Authorization': KEY[idx % len(KEY)],
                "Accept": "application/vnd.api+json"}
            print(i, 'match data API 호출')
            match_url = f"https://api.pubg.com/shards/steam/matches/{i}" 
            match_response = requests.get(match_url, headers=headers)
            match_response.raise_for_status()
            
            if match_response.status_code == 200 : 
                match_data_json = match_response.json()
            else:
                print('!!!!API 호출 에러!!!!')

                
            for j in range(len(match_data_json['included'])) :
                
                # player 테이블 저장
                if j == 0:
                    createAt = match_data_json['data']['attributes']['createdAt']
                    p, p_created = players.objects.get_or_create(
                        account_id=account_id,
                        player_name=user_name,
                        shard_id=user_server,
                        match_id=i,
                        created_at=createAt)
                    
                    if p_created:
                        print("players 데이터 저장")

                    else:
                        print("players 중복 데이터 PASS")
                    print(account_id, i)
                    get_player = players.objects.get(account_id=account_id, match_id=i)
                    players_table = get_player.id
                    # weapon_masterys 데이터 삭제
                    try:
                        w_mastery = weapon_masterys.objects.filter(account_id=account_id)
                        w_mastery.delete()
                        print("기존 weapon_masterys 레코드 삭제")
                    except weapon_masterys.DoesNotExist:
                        print("기존 weapon_masterys 레코드 없음")

                    # weapon_mastery API 호출
                    mastery_url = f"https://api.pubg.com/shards/kakao/players/{account_id}/weapon_mastery"
                    weapon_mastery_response = requests.get(mastery_url, headers=headers)
                    
                    if weapon_mastery_response.status_code == 200:
                        weapon_mastery_data_json = weapon_mastery_response.json()
                        weapon_mastery_data_list = weapon_mastery_data_json['data']['attributes']['weaponSummaries']
                        
                        # 경험치를 기준으로 무기 정렬
                        sorted_weapons = sorted(weapon_mastery_data_list.items(), key=lambda x: x[1]['XPTotal'], reverse=True)
                        
                        # 상위 3개 무기 컬럼에 선언
                        top3_weapons = sorted_weapons[:3]
                        first_weapon_name = top3_weapons[0][0].split('_')[-2]
                        first_weapon_XPtotal = top3_weapons[0][1]['XPTotal']
                        second_weapon_name = top3_weapons[1][0].split('_')[-2]
                        second_weapon_XPtotal = top3_weapons[1][1]['XPTotal']
                        third_weapon_name = top3_weapons[2][0].split('_')[-2]
                        third_weapon_XPtotal = top3_weapons[2][1]['XPTotal']

                        df = pd.DataFrame()

                        for l in weapon_mastery_data_list.keys() : 
                            weapon_summary = weapon_mastery_data_list[l]
                            xptotal = weapon_summary['XPTotal']
                            most_defeats_in_a_game = weapon_summary['StatsTotal']['MostDefeatsInAGame']
                            defeats = weapon_summary['StatsTotal']['Defeats']
                            most_damage_player_in_a_game = weapon_summary['StatsTotal']['MostDamagePlayerInAGame']
                            damage_player = weapon_summary['StatsTotal']['DamagePlayer']
                            most_headshots_in_a_game = weapon_summary['StatsTotal']['MostHeadShotsInAGame']
                            headshots = weapon_summary['StatsTotal']['HeadShots']
                            longest_defeat = weapon_summary['StatsTotal']['LongestDefeat']
                            long_range_defeats = weapon_summary['StatsTotal']['LongRangeDefeats']
                            weapon_kills = weapon_summary['StatsTotal']['Kills']
                            most_kills_in_a_game = weapon_summary['StatsTotal']['MostKillsInAGame']
                            groggies = weapon_summary['StatsTotal']['Groggies']
                            most_groggies_in_a_game = weapon_summary['StatsTotal']['MostGroggiesInAGame']
                        
                            new_data = {
                                'Weapon': l,
                                'XPTotal': xptotal,
                                'Most Defeats in a Game': most_defeats_in_a_game,
                                'Defeats': defeats,
                                'Most Damage Player in a Game': most_damage_player_in_a_game,
                                'Damage Player': damage_player,
                                'Most Headshots in a Game': most_headshots_in_a_game,
                                'Headshots': headshots,
                                'Longest Defeat': longest_defeat,
                                'Long Range Defeats': long_range_defeats,
                                'Kills': weapon_kills,
                                'Most Kills in a Game': most_kills_in_a_game,
                                'Groggies': groggies,
                                'Most Groggies in a Game': most_groggies_in_a_game}
                            
                            df = df.append(new_data, ignore_index=True)
                            # 지정사수소총 DMR
                            df.loc[df['Weapon'].isin(['Item_Weapon_SKS_C', 'Item_Weapon_FNFal_C', 'Item_Weapon_Mini14_C', 'Item_Weapon_Mk12_C', 'Item_Weapon_Mk14_C', 'Item_Weapon_QBU88_C', 'Item_Weapon_VSS_C']), '무기분류'] = 'DMR'
                            # 저격소총 SR
                            df.loc[df['Weapon'].isin(['Item_Weapon_AWM_C', 'Item_Weapon_Kar98k_C', 'Item_Weapon_L6_C', 'Item_Weapon_M24_C', 'Item_Weapon_Mosin_C', 'Item_Weapon_Winchester_C', 'Item_Weapon_Win1894_C']), '무기분류'] = 'SR'
                            # 기관단총 SMG
                            df.loc[df['Weapon'].isin(['Item_Weapon_Thompson_C', 'Item_Weapon_BizonPP19_C', 'Item_Weapon_UZI_C', 'Item_Weapon_MP5K_C', 'Item_Weapon_MP9_C', 'Item_Weapon_P90_C', 'Item_Weapon_UMP_C', 'Item_Weapon_Vector_C']), '무기분류'] = 'SMG'
                            # 경기관총 LMG
                            df.loc[df['Weapon'].isin(['Item_Weapon_DP28_C', 'Item_Weapon_M249_C', 'Item_Weapon_MG3_C']), '무기분류'] = 'LMG'
                            # 산탄총 SG
                            df.loc[df['Weapon'].isin(['Item_Weapon_Saiga12_C', 'Item_Weapon_DP12_C', 'Item_Weapon_OriginS12_C', 'Item_Weapon_Winchester_C', 'Item_Weapon_Berreta686_C', 'Item_Weapon_Sawnoff_C']), '무기분류'] = 'SG'
                            # 권총
                            df.loc[df['Weapon'].isin(['Item_Weapon_DesertEagle_C', 'Item_Weapon_G18_C', 'Item_Weapon_M1911_C', 'Item_Weapon_M9_C', 'Item_Weapon_NagantM1895_C', 'Item_Weapon_Rhino_C', 'Item_Weapon_vz61Skorpion_C']), '무기분류'] = '권총'
                            # 기타 MISC
                            df.loc[df['Weapon'].isin(['Item_Weapon_Crossbow_C']), '무기분류'] = 'MISC'
                            # 돌격소총 AR
                            df.loc[df['Weapon'].isin(['Item_Weapon_HK416_C', 'Item_Weapon_AK47_C', 'Item_Weapon_BerylM762_C', 'Item_Weapon_SCAR-L_C', 'Item_Weapon_ACE32_C', 'Item_Weapon_QBZ95_C', 'Item_Weapon_M16A4_C', 'Item_Weapon_Groza_C', 'Item_Weapon_AUG_C', 'Item_Weapon_Mk47Mutant_C', 'Item_Weapon_FAMASG2_C', 'Item_Weapon_G36C_C', 'Item_Weapon_K2_C']), '무기분류'] = 'AR'

                        features = df.drop(['Weapon', 'Most Defeats in a Game', 'Most Damage Player in a Game','Most Headshots in a Game', 'Most Kills in a Game', 'Most Groggies in a Game'], axis=1) 

                        
                        weapon_categories = features['무기분류']  # 무기 카테고리 열 이름에 맞게 수정
                        user_features = ['XPTotal', 'Defeats', 'Damage Player', 'Headshots', 'Longest Defeat', 'Long Range Defeats', 'Kills', 'Groggies'] # 사용자 특징 열 이름에 맞게 수정

                        group_by_weapon = features.groupby(weapon_categories).mean().reset_index()

                        scaler = MinMaxScaler()
                        scaled_features = scaler.fit_transform(group_by_weapon[user_features])

                        k = 3
                        kmeans = KMeans(n_clusters=k, random_state=42)
                        kmeans.fit(scaled_features)

                        group_by_weapon['Cluster'] = kmeans.labels_
                        weapon_mapping = {l: category for l, category in enumerate(group_by_weapon.index)}
                        group_by_weapon['우선순위'] = group_by_weapon['Cluster'].map(weapon_mapping)

                        result = {
                            '분류': group_by_weapon
                        }

                        cluster_counts = pd.Series(kmeans.labels_).value_counts()

                        if cluster_counts[0] >= cluster_counts[1] and cluster_counts[0] >= cluster_counts[2]:
                            user_weapon_type = '저격수'
                        elif cluster_counts[1] >= cluster_counts[0] and cluster_counts[1] >= cluster_counts[2]:
                            user_weapon_type = '돌격수'
                        else:
                            user_weapon_type = '근접킬러'

                        result['유저무기유형'] = user_weapon_type

                        get_player = players.objects.get(account_id=account_id, match_id=i)
                        players_table = get_player.id
                        
                        w_mastery = weapon_masterys(
                            players_table = players.objects.get(id=players_table),
                            account_id = account_id,
                            first_weapon_name = first_weapon_name,
                            first_weapon_XPtotal = first_weapon_XPtotal,
                            second_weapon_name = second_weapon_name,
                            second_weapon_XPtotal = second_weapon_XPtotal,
                            third_weapon_name = third_weapon_name,
                            third_weapon_XPtotal = third_weapon_XPtotal,
                            weapon_cluster = user_weapon_type
                        )
                        try:
                            with transaction.atomic():
                                w_mastery.save()
                                print('weapon_mastery 저장')
                        except IntegrityError as e:
                            print("IntegrityError : ", e)
                            print('weapon_mastery 저장 오류')
                            pass


                get_player = players.objects.get(account_id=account_id, match_id=i)
                players_table = get_player.id

                # match_summary 테이블 저장
                if match_data_json['included'][j]['type'] == 'asset':
                    createAt = match_data_json['data']['attributes']['createdAt']
                    gameMode = match_data_json['data']['attributes']['gameMode']
                    mapname = match_data_json['data']['attributes']['mapName']
                    duration = match_data_json['data']['attributes']['duration']
                    match_type = match_data_json['data']['attributes']['matchType']
                    asset_url = match_data_json['included'][j]['attributes']['URL']

                    m_summary, m_created = match_summarys.objects.get_or_create(
                        players_table=players.objects.get(id=players_table),
                        match_id=i,
                        defaults={
                            'created_at': createAt,
                            'game_mode': gameMode,
                            'map_name': mapname,
                            'duration': duration,
                            'match_type': match_type,
                            'asset_url': asset_url,
                        }
                    )
                    if m_created:
                        print("m_summary 데이터 저장")
                    else:
                        print("m_summary 중복 데이터 PASS")
        

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

                    m_participant, mp_created = match_participants.objects.get_or_create(
                        players_table=players.objects.get(id=players_table),
                        match_id=i,
                        player_name=player_name,
                        account_id=accountId,
                        defaults={
                            'team_ranking': team_ranking,
                            'dbnos': DBNOs,
                            'assists': assists,
                            'damage_dealt': damageDealt,
                            'headshot_kills': headshotkills,
                            'kills': kills,
                            'longest_kill': longestkill,
                            'team_kills': teamkills,
                            'ride_distance': rideDistance,
                            'swim_distance': swimDistance,
                            'walk_distance': walkDistance,
                        }
                    )
                    if mp_created:
                        print("m_participant 데이터 저장")
                    else:
                        print("m_participant 중복 데이터 PASS")

    except requests.exceptions.RequestException as e:
        print('API 요청 오류:', e)
        return render(request, 'main.html')
    
    # return redirect(f'/profile/?user_server={service}&?user_name={user}')
    return HttpResponseRedirect(reverse('services:profile') + f'?service={service}&user_name={user}')
