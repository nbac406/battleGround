from django.shortcuts import render, redirect
import requests
from config.settings.prod import KEY
from .models import players, match_summarys, weapon_masterys, match_participants, position_logs, kill_logs, weapons, weapon_parts, maps
from django.db import transaction, IntegrityError
from datetime import datetime, timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import pandas as pd
import warnings
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Sum, Count


def index(request):
    return render(request, 'main.html')

def profile(request):
    if request.method == 'GET':
        service = request.GET.get("service")
        user_name = request.GET.get("user_name")
        
        current_date = datetime.now()
        past_date = current_date - timedelta(days=30)
        players.objects.filter(created_at__lt=past_date).delete()
        
        user_data = players.objects.filter(player_name=user_name)
        user_data_match_ids = user_data.values_list('match_id', flat=True)

        try:
            user_account_id = user_data.first().account_id
            weapon_masterys_data = weapon_masterys.objects.filter(account_id=user_account_id).first()
        except:
            user_account_id = None
            weapon_masterys_data = None

        match_participant_data = []
        
        for match_id in user_data_match_ids:
            game_mode = match_summarys.objects.filter(match_id=match_id).values('game_mode')
            map_name = match_summarys.objects.filter(match_id=match_id).values('map_name')
            match_participant = match_participants.objects.filter(match_id=match_id, player_name=user_name)

            m_data = {
                'match_participant_data': match_participants.objects.filter(match_id=match_id, player_name=user_name),
                'game_mode' : game_mode,
                'map_name' : map_name,
                'created_at': players.objects.filter(match_id=match_id, player_name=user_name).values('created_at').first(),
            }

            if match_participant:
                match_participant_data.append(m_data)
                match_participant_data = sorted(match_participant_data, key=lambda x: x['created_at']['created_at'], reverse=True)
        
        if match_participant_data:
            paginator = Paginator(match_participant_data, 10)  # 한 페이지에 10개씩 표시하도록 설정
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
        else:
            page = None


        # solo k/d 구하기
        solo_kills_sum = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).aggregate(Sum('kills'))['kills__sum']
        
        solo_death_sum = match_participants.objects.filter(
            player_name=user_name,
            team_ranking__gte=2,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).count()

        if solo_death_sum != 0:
            solo_kd = solo_kills_sum/solo_death_sum
        else:
            solo_kd = None

        # duo k/d 구하기
        duo_kills_sum = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).aggregate(Sum('kills'))['kills__sum']
        
        duo_death_sum = match_participants.objects.filter(
            player_name=user_name,
            team_ranking__gte=2,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).count()

        if duo_death_sum != 0:
            duo_kd = duo_kills_sum/duo_death_sum
        else:
            duo_kd = None

        # squad k/d 구하기
        squad_kills_sum = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).aggregate(Sum('kills'))['kills__sum']
        
        squad_death_sum = match_participants.objects.filter(
            player_name=user_name,
            team_ranking__gte=2,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).count()

        if squad_death_sum != 0:
            squad_kd = squad_kills_sum/squad_death_sum
        else:
            squad_kd = None

        # solo 1등 비율 구하기
        solo_win_count = match_participants.objects.filter(
            player_name=user_name,
            team_ranking=1,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).count()

        solo_match_total = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).count()

        if solo_match_total != 0:
            solo_win_ratio = (solo_win_count/solo_match_total) * 100
        else:
            solo_win_ratio = None

        # duo 1등 비율 구하기
        duo_win_count = match_participants.objects.filter(
            player_name=user_name,
            team_ranking=1,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).count()

        duo_match_total = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).count()

        if duo_match_total != 0:
            duo_win_ratio = (duo_win_count/duo_match_total) * 100
        else:
            duo_win_ratio = None

        # squad 1등 비율 구하기
        squad_win_count = match_participants.objects.filter(
            player_name=user_name,
            team_ranking=1,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).count()

        squad_match_total = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).count()

        if squad_match_total != 0:
            squad_win_ratio = (squad_win_count/squad_match_total) * 100
        else:
            squad_win_ratio = None

        # solo Top10 비율
        solo_top10_count = match_participants.objects.filter(
            player_name=user_name,
            team_ranking__range=(2, 10),
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).count()

        if solo_match_total != 0:
            solo_top10_ratio = (solo_top10_count/solo_match_total) * 100
        else:
            solo_top10_ratio = None

        # duo Top10 비율 구하기
        duo_top10_count = match_participants.objects.filter(
            player_name=user_name,
            team_ranking__range=(2, 10),
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).count()

        if duo_match_total != 0:
            duo_top10_ratio = (duo_top10_count/duo_match_total) * 100
        else:
            duo_top10_ratio = None

        # squad Top10 비율 구하기
        squad_top10_count = match_participants.objects.filter(
            player_name=user_name,
            team_ranking__range=(2, 10),
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).count()

        if squad_match_total != 0:
            squad_top10_ratio = (squad_top10_count/squad_match_total) * 100
        else:
            squad_top10_ratio = None

        # solo 평균 딜량
        solo_deal_avr =  match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).aggregate(Avg('damage_dealt'))['damage_dealt__avg']

        # duo 평균 딜량
        duo_deal_avr =  match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).aggregate(Avg('damage_dealt'))['damage_dealt__avg']

        # squad 평균 딜량
        squad_deal_avr =  match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).aggregate(Avg('damage_dealt'))['damage_dealt__avg']

        # solo 헤드샷 비율
        solo_headshot_sum = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).aggregate(Sum('headshot_kills'))['headshot_kills__sum']

        if solo_kills_sum is not None and solo_headshot_sum is not None and solo_kills_sum > 0:
            solo_headshot_ratio = (solo_headshot_sum/solo_kills_sum) * 100
        else:
            solo_headshot_ratio = None

        # duo 헤드샷 비율
        duo_headshot_sum = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).aggregate(Sum('headshot_kills'))['headshot_kills__sum']

        if duo_kills_sum is not None and duo_headshot_sum is not None and duo_kills_sum > 0:
            duo_headshot_ratio = (duo_headshot_sum/duo_kills_sum) * 100
        else:
            duo_headshot_ratio = None

        # squad 헤드샷 비율
        squad_headshot_sum = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).aggregate(Sum('headshot_kills'))['headshot_kills__sum']

        if squad_kills_sum is not None and squad_headshot_sum is not None and squad_kills_sum > 0:
            squad_headshot_ratio = (squad_headshot_sum/squad_kills_sum) * 100
        else:
            squad_headshot_ratio = None

        # solo 최대킬
        solo_max_kill_data = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).order_by('-kills').first()

        if solo_max_kill_data:
            solo_max_kill = solo_max_kill_data.kills
        else:
            solo_max_kill = None


        # duo 최대킬
        duo_max_kill_data = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).order_by('-kills').first()

        if duo_max_kill_data:
            duo_max_kill = duo_max_kill_data.kills
        else:
            duo_max_kill = None

        # squad 최대킬
        squad_max_kill_data = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).order_by('-kills').first()

        if squad_max_kill_data:
            squad_max_kill = squad_max_kill_data.kills
        else:
            squad_max_kill = None

        # solo 킬 최장거리
        solo_max_kill_range_data = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='solo').values('match_id')
        ).order_by('-longest_kill').first()

        if solo_max_kill_range_data:
            solo_max_kill_range = solo_max_kill_range_data.longest_kill
        else:
            solo_max_kill_range = None

        # duo 킬 최장거리
        duo_max_kill_range_data = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='duo').values('match_id')
        ).order_by('-longest_kill').first()

        if duo_max_kill_range_data:
            duo_max_kill_range = duo_max_kill_range_data.longest_kill
        else:
            duo_max_kill_range = None

        # squad 킬 최장거리
        squad_max_kill_range_data = match_participants.objects.filter(
            player_name=user_name,
            match_id__in=match_summarys.objects.filter(game_mode='squad').values('match_id')
        ).order_by('-longest_kill').first()

        if squad_max_kill_range_data:
            squad_max_kill_range = squad_max_kill_range_data.longest_kill
        else:
            squad_max_kill_range = None


        solo_data_overall = {
            'solo_kd': solo_kd,
            'solo_win_ratio': solo_win_ratio,
            'solo_top10_ratio': solo_top10_ratio,
            'solo_deal_avr': solo_deal_avr,
            'solo_headshot_ratio': solo_headshot_ratio,
            'solo_max_kill': solo_max_kill,
            'solo_max_kill_range': solo_max_kill_range,
        }

        duo_data_overall = {
            'duo_kd': duo_kd,
            'duo_win_ratio': duo_win_ratio,
            'duo_top10_ratio': duo_top10_ratio,
            'duo_deal_avr': duo_deal_avr,
            'duo_headshot_ratio': duo_headshot_ratio,
            'duo_max_kill': duo_max_kill,
            'duo_max_kill_range': duo_max_kill_range,
        }

        squad_data_overall = {
            'squad_kd': squad_kd,
            'squad_win_ratio': squad_win_ratio,
            'squad_top10_ratio': squad_top10_ratio,
            'squad_deal_avr': squad_deal_avr,
            'squad_headshot_ratio': squad_headshot_ratio,
            'squad_max_kill': squad_max_kill,
            'squad_max_kill_range': squad_max_kill_range,
        }

        data = {
            'user_name': user_name,
            'user_service': service,
            'match_participant_data' : match_participant_data,
            'page': page,
            'solo_data': solo_data_overall,
            'duo_data': duo_data_overall,
            'squad_data': squad_data_overall,
            'weapon_mastery_data': weapon_masterys_data,
        }

        return render(request, 'profile.html', data)

    return redirect('services:index')

def profile_update(request):
    warnings.filterwarnings('ignore')
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

        for idx, n in enumerate(match_history):
            i = n.get('id')
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

                    get_player = players.objects.get(account_id=account_id, match_id=i)
                    players_table = get_player.id

                    if idx == 0:
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
                        else:
                            print('weapon_mastery API 호출 에러')


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
                    players_table=players.objects.get(id=players_table)

                    m_summary, m_created = match_summarys.objects.get_or_create(
                        match_id=i,
                        defaults={
                            'players_table': players_table,
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
        

                elif match_data_json['included'][j]['type'] == 'participant' and 'ai' not in match_data_json['included'][j]['attributes']['stats']['playerId']:

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
                    players_table=players.objects.get(id=players_table)

                    m_participant, mp_created = match_participants.objects.get_or_create(
                        match_id=i,
                        account_id=accountId,
                        defaults={
                            'players_table': players_table,
                            'player_name': player_name,
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
                        print("m_participant 신규 데이터 저장")
                    else:
                        print("m_participant 중복 데이터 PASS")
                        pass

    except requests.exceptions.RequestException as e:
        print('API 요청 오류:', e)
        return render(request, 'main.html')

    return HttpResponseRedirect(reverse('services:profile') + f'?service={service}&user_name={user}')

def match_log_map(request):
    if request.method == 'GET':
        match_id = request.GET.get("match_id")
        account_id = request.GET.get("account_id")
        map_name = request.GET.get("map_name")

        if map_name == 'Baltic_Main':
            map_code_name = 'Erangel'
        elif map_name == 'Desert_Main':
            map_code_name = 'Miramar'
        elif map_name == 'Savage_Main':
            map_code_name = 'Sanhok'
        elif map_name == 'DihorOtok_Main':
            map_code_name = 'Vikendi'
        elif map_name == 'Tiger_Main':
            map_code_name = 'Taego'
        elif map_name == 'Kiki_Main':
            map_code_name = 'Deston'

        get_asset_url = match_summarys.objects.filter(match_id=match_id).values('asset_url').first()
        asset_url = get_asset_url['asset_url']

        try:
            logs = requests.get(asset_url).json()
        except:
            logs = None
            
        record = False
        positions = []
        kills = []

        get_player = players.objects.get(account_id=account_id, match_id=match_id)
        players_table = get_player.id
        player_name = get_player.player_name

        if not position_logs.objects.filter(account_id=account_id, match_id=match_id).exists() and not kill_logs.objects.filter(match_id=match_id).exists():
            for log in logs[1:] :
                if log['_T'] == 'LogMatchStart' :
                    start_time = datetime.strptime(log['_D'], '%Y-%m-%dT%H:%M:%S.%fZ')
                if 'character' in log.keys() :
                    if log['_T'] == 'LogParachuteLanding' and log['character']['accountId'] == account_id:
                        record = True
                    if log['character']['accountId'] == account_id and record and log['_T'] in['LogParachuteLanding', 'LogPlayerPosition'] :
                        try:
                            p_log, p_log_created = position_logs.objects.get_or_create(
                                account_id = account_id,
                                match_id = match_id,
                                event_time = (datetime.strptime(log['_D'], '%Y-%m-%dT%H:%M:%S.%fZ') - start_time).seconds,
                                defaults = {
                                    'players_table' : players.objects.get(id=players_table),
                                    'player_name' : log['character']['name'],
                                    'location_x' : log['character']['location']['x'],
                                    'location_y' : log['character']['location']['y'],
                                }
                            )
                            if p_log_created:
                                print('position_log 데이터 저장')
                            else:
                                print('position_log 중복 데이터 PASS')

                        except Exception as e:
                            print(e)

                elif log['_T'] == 'LogPlayerKillV2' :
                    killer_filter = log['killer']['accountId'] ==  account_id if log['killer'] != None else False
                    if log['victim']['accountId'] ==  account_id or killer_filter :
                        try:
                            k_log, k_log_created = kill_logs.objects.get_or_create(
                                match_id = match_id,
                                killer_name = None if log['killer'] == None else log['killer']['name'],
                                victim_name = log['victim']['name'],
                                defaults = {
                                    'players_table' : players.objects.get(id=players_table),
                                    'killer_account_id' : None if log['killer'] == None else log['killer']['accountId'],
                                    'victim_account_id' : log['victim']['accountId'],
                                    'killer_x' : None if log['killer'] == None else log['killer']['location']['x'],
                                    'killer_y' : None if log['killer'] == None else log['killer']['location']['y'],
                                    'victim_x' : log['victim']['location']['x'],
                                    'victim_y' : log['victim']['location']['y'],
                                    'event_time' : (datetime.strptime(log['_D'], '%Y-%m-%dT%H:%M:%S.%fZ') - start_time).seconds,
                                }
                            )
                            if k_log_created:
                                print('kill_log 데이터 저장')
                            else:
                                print('kill_log 중복 데이터 PASS')

                        except Exception as e:
                            print(e)
        else:
            print('이미 존재하는 Log 데이터 입니다.')
        
        positions = position_logs.objects.filter(players_table=players_table)
        kills = kill_logs.objects.filter(match_id=match_id).order_by('event_time')

        data = {
            'positions' : positions,
            'kills' : kills,
            'map_name' : map_code_name,
            'player_name' : player_name,
        }

    return render(request, 'map.html', data)

def map_analysis(request):
    return render(request, 'map_analysis.html')
from .models import weapons

def weapon_analysis(request):
    weapons_tier1 = weapons.objects.filter(weapon_tier=1).exclude(weapon_type='권총')
    weapons_tier2 = weapons.objects.filter(weapon_tier=2).exclude(weapon_type='권총')
    weapons_tier3 = weapons.objects.filter(weapon_tier=3).exclude(weapon_type='권총')
    weapons_tier4 = weapons.objects.filter(weapon_tier=4).exclude(weapon_type='권총')
    weapons_tier5 = weapons.objects.filter(weapon_tier=5).exclude(weapon_type='권총')
    weapons_no_tier = weapons.objects.filter(weapon_tier__isnull=True).exclude(weapon_type='권총')

    context = {
        'weapons_tier1': weapons_tier1,
        'weapons_tier2': weapons_tier2,
        'weapons_tier3': weapons_tier3,
        'weapons_tier4': weapons_tier4,
        'weapons_tier5': weapons_tier5,
        'weapons_no_tier': weapons_no_tier,
    }

    return render(request, 'weapon_analysis.html', context)

from google.cloud import storage

def get_map_image_url(request):
    if request.method == "POST" and "start" in request.POST and "destination" in request.POST:
        start = request.POST["start"]
        destination = request.POST["destination"]
        map_name = request.POST["mapName"]
        if map_name == 'Erangel':
            map_code_name = 'Baltic_Main'
        elif map_name == 'Miramar':
            map_code_name = 'Desert_Main'
        elif map_name == 'Sanhok':
            map_code_name = 'Savage_Main'
        elif map_name == 'Vikendi':
            map_code_name = 'DihorOtok_Main'
        elif map_name == 'Taego':
            map_code_name = 'Tiger_Main'
        elif map_name == 'Deston':
            map_code_name = 'Kiki_Main'
        
        # 출발지와 도착지를 이용하여 이미지 URL 생성 (임의로 예시를 작성합니다)
        image_url = maps.objects.filter(map_name=map_code_name, start_point=start, end_point=destination).values('image_url').first()

        # 생성된 이미지 URL을 JSON 형식으로 응답
        return JsonResponse({"imageURL": image_url['image_url']})
    else:
        # 요청이 올바르지 않은 경우 에러 응답
        return JsonResponse({"error": "Invalid request"}, status=400)

def get_image_url(bucket_name, file_path):
    client = storage.Client.from_service_account_json('./playdata-2-1e60a2f219de.json')
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)
    return blob.public_url


def weapons_detail(request, weapon_name):
    specific_weapon = weapons.objects.get(weapon_name=weapon_name)
    weapon_image_url = get_image_url('playdata2', f'images/{specific_weapon.weapon_name}.jpg')
    weapon_parts_type_all = [
        {'name': '탄창', 'parts': weapon_parts.objects.filter(weapon_name=weapon_name, parts_type='탄창')},
        {'name': '조준경', 'parts': weapon_parts.objects.filter(weapon_name=weapon_name, parts_type='조준경')},
        {'name': '총구', 'parts': weapon_parts.objects.filter(weapon_name=weapon_name, parts_type='총구')},
        {'name': '개머리판', 'parts': weapon_parts.objects.filter(weapon_name=weapon_name, parts_type='개머리판')},
        {'name': '손잡이', 'parts': weapon_parts.objects.filter(weapon_name=weapon_name, parts_type='손잡이')},
    ]

    context = {
        'weapon': specific_weapon,
        'weapon_image_url': weapon_image_url,
        'weapon_parts_type_all': weapon_parts_type_all
    }
    return render(request, 'weapon_analysis_detail.html', context)
