# -*- coding: utf-8 -*-
import datetime
import requests
import pandas as pd
import numpy as np
import time
import multi2 as am

# 사용자 정의 함수들

def get_user(account_id, api) :
    header = {
        'Authorization': api,
        'Accept' : 'application/vnd.api+json'
    }
    url = f"https://api.pubg.com/shards/kakao/players/{account_id}"
    try :
        request = requests.get(url, headers = header)
    except :
        return 'request error'
    
    # 오류 발생했을 경우의 예외처리
    if request.status_code != 200 :
        return 'status not 200 error'
    
    if 'errors' in request.json().keys() :
        return 'errors in request error'
    
    try :
        return request.json()['data']['relationships']['matches']['data']
    except :
        return 'has not matches error'

def get_match(match_id, author) :
    header = {
        'Authorization': author,
        'Accept' : 'application/vnd.api+json'
    }
    url = f"https://api.pubg.com/shards/kakao/matches/{match_id}"
    try :
        request = requests.get(url, headers = header)
    except :
        return 'request error'
    
    # 오류 발생했을 경우의 예외처리
    if request.status_code != 200 :
        return 'status not 200 error'
    
    if 'errors' in request.json().keys() :
        return 'errors in request error'
    
    try :
        row = {'match_id' : request.json()['data']['id'],
               'map_name' : request.json()['data']['attributes']['mapName'],
               'game_mode' : request.json()['data']['attributes']['gameMode'],
               'created_at' : request.json()['data']['attributes']['createdAt'],
               'shard_id' : request.json()['data']['attributes']['shardId'],
               'asset_url' : list(filter(lambda x : x['type'] == 'asset', request.json()['included']))[0]['attributes']['URL']
              }
        return [row]
    except :
        return 'has not matches error'

# api
author1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMjg0ZDBjMC1lMGQ5LTAxM2ItNGVlNS0wMjJlZGE2MTJmNmMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NDI0NjU0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFwaTEifQ.FoLqbKF83KfdOo42OvkoLlswFp78ftcXFeP9akV8R4g' #형식
author2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiNjA3NjExMC1lMThkLTAxM2ItNGVlOC0wMjJlZGE2MTJmNmMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTAyMjM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImZvcl9hZGRfcmVxdWVzIn0._ZnA0opuvzWy8ONFTOO6wq5WHA90lw3aQD9SsABmM_M' #형식
author3 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmYzA1NjA5MC1lMTlkLTAxM2ItYWIwZC00YWQ1NTRmZjEzNWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTA5MjI4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii02N2NjOWEzZC1jNzk5LTQ5MjgtYWZhOS03ZGExZWRiMjA0ZmQifQ.2NVhbJS3pjOp-SJLRH_pOYf3p3Zn_hAh6fxzO5-3NN8' #형식
author4 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNDM1Nzc5MC1lMTllLTAxM2ItNDRhYi01NmE0MmY0YzFkNGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTA5MjY4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii01MWYxYjNhNC05YTJkLTQ1MzAtOWIyMy03YjU4YzI5NTZmZTIifQ.XxqN69vTIwkdgRDBxQ2mAHHWkj3Rc3xgsreJhi0KvO4' #형식
author5 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNDNiMmFkMC1lMGUyLTAxM2ItNWVhYS00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NDI4NTIzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InByb2plY3RfZ2FtZSJ9.rDPrdCT3GOWRp9UEWasFRI7EuE_HlnDyvGq_eENzzak' # 재규
author6 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3YjViOWQ2MC1lMWE0LTAxM2ItNDRhZC01NmE0MmY0YzFkNGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEyMDE4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii02ODhiY2QyNi0yZDdiLTRlNDMtYTE0NC0yOWUwNGRiOTNiMmEifQ.I2rwkm5XYxyjktRKvFJNb4jTRO28FjHzD7JEK8C-dGo' # 재규
author7 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxZTg2NmE2MC1lMWE1LTAxM2ItYzg2Mi00Mjg1NWU5MDJkNTYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEyMjkyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImRhdGEyIn0.ANcRT57sj3kxDNwvbt_1kHvYRwafpKXXB1juyc1wZ3w' # 혜규
author8 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwZDJiYjMwMC1lMWE1LTAxM2ItNDRiMC01NmE0MmY0YzFkNGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEyMjYzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05OTQyOTIxMy00YjlkLTQ0MTEtYjI4MS1hOWIwMjBlNjUxYjYifQ.camj7sp5qGdzX11nGeI56nPFNBYqoBzQUwvL0gOXNY0' # 혜규
author13 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjMzA2ZTAyMC0wMDhjLTAxM2MtODI4YS00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg4OTEwMzE3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii04Nzk4YjM4Mi1iNzlmLTQ4NDMtODQ0Yi1jMzU2OTkxNWJjYTQifQ.ka7oEx52wyZMX2DT63eJaOEqjxXqxbLVPGjLCQ6zmbI' # 형식
author14 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiZDI0NTMyMC0wMDhjLTAxM2MtZDZiMC0xYWE5ZThmZjAwZmMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg4OTEwMzA3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii04NGM0MjhjMi03OTc3LTRjYTMtOGRjZC1iYWY3NWQ3YmQwNGMifQ.0g0MS6EV2kofC9GzZpcFvrOSQyJexqgQmrUWoiWEqNs' # 형식

# 사용중
# author9 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwZTQ5MjFhMC1lMWE4LTAxM2ItNWViMi00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEzNTUzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImRhdGFncm91bmQyIn0.aQ8DgPRZHy3zG9J4RKv3bM76HSDr0g7UK_llq3NQaOs' # 정우형
# author10 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjNjVkNzliMC1kYjMwLTAxM2ItYzgwOS00Mjg1NWU5MDJkNTYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg0ODAyNjE1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImRhdGFncm91bmQifQ.dP4R75BLmPNgHXE8RVak6kmbETnhHuKY-56yD7S1RtI' # 정우형
# author11 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5MmEzOGYzMC1lMWE3LTAxM2ItYzg2NC00Mjg1NWU5MDJkNTYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEzMzQ2LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1hZjdmNzc5NC1lMzU2LTRjZjUtYTU5Yi0yNDUzNzlkNjg2MjAifQ._JAnysrJ6QNmqw2DmDf0O62HfL77caOlIrsTWerLzFo' # 종범이형
# author12 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTNhYzViMC1kYjQ3LTAxM2ItNWU2YS00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg0ODEyMjk3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii04ZWU0NjRkNi1jNjdkLTQyMDEtOGIzNC02N2I4YjUwOWJhYjgifQ.KiEz10CpYXFS2r4SsWq8aizag2oEAy6KtbH0e2TQH7s' # 종범이형

# 사용할 api
apis = [
    author1,
    author2,
    author3,
    author4,
    author5,
    author6,
    author7,
    author8,
    author13,
    author14,
]

while True :
    # api 호출속도
    count_apis = len(apis)
    max_tries = count_apis * 10
    tries = 0
    cur_minute = datetime.datetime.today().minute

    # api 교차사용
    num_api = 0

    # 유저 정보 호출 후 랜덤으로 유저 100명 요청
    users = pd.read_parquet("parquets/target_users.parquet")
    target_size = 50 # test
    users_list = users.index.to_numpy()
    np.random.shuffle(users_list)

    users_matches = []
    for index, row in users.iloc[users_list].iterrows() :

        # 원하는 갯수 달성 시 루프 종료
        if target_size == 0 :
            break
        
        # 아웃 인덱싱 방지
        if num_api == count_apis :
            num_api = 0

        # 제한 속도 걸렸을 경우 속도 제한
        if tries == max_tries :
            sleep_second = 60 - datetime.datetime.today().second
            time.sleep(sleep_second)

        # 매 분마다 속도제한 초기화
        if cur_minute != datetime.datetime.today().minute :
            cur_minute = datetime.datetime.today().minute
            tries = 0

        api = apis[num_api]
        account_id = row['account_id']
        result = get_user(account_id, api)
        if type(result) == list :
            users_matches += result
            target_size -= 1

        tries += 1
        num_api += 1

    # 수집한 유저의 매치들 중에서 없는 경기들만 추출
    user_match_df = pd.DataFrame(users_matches)
    user_match_df = user_match_df.drop(columns = ['type'])
    user_match_df = user_match_df.drop_duplicates('id')
    user_match_df = user_match_df.rename(columns = {'id' : 'match_id'})

    match_summary = pd.read_parquet('parquets/match_summary.parquet')
    df = pd.merge(user_match_df, match_summary, how = 'left', on = 'match_id')
    match_target = df[df['map_name'].isnull()][['match_id']].copy()
    del user_match_df
    del df

    rows = []
    for index, row in match_target.iterrows() :

        # 아웃 인덱싱 방지
        if num_api == count_apis :
            num_api = 0

        # 제한 속도 걸렸을 경우 속도 제한
        if tries == max_tries :
            sleep_second = 60 - datetime.datetime.today().second
            time.sleep(sleep_second)

        # 매 분마다 속도제한 초기화
        if cur_minute != datetime.datetime.today().minute :
            cur_minute = datetime.datetime.today().minute
            tries = 0

        api = apis[num_api]
        match_id = row['match_id']
        result = get_match(match_id, api)
        if type(result) == list :
            rows += result

        tries += 1
        num_api += 1
    try :
        new_match_summary = pd.DataFrame(rows)
        nms = new_match_summary[['match_id', 'map_name', 'game_mode', 'created_at', 'shard_id']]
        pd.concat([match_summary, nms], axis = 0).reset_index(drop = True).to_parquet('parquets/match_summary.parquet')
    
    except :
        continue

    get_log_list = []
    for index, row in new_match_summary.iterrows() :
        rows = {'match_id' : row['match_id'],
                'asset_url' : row['asset_url'],
                }
        get_log_list.append(rows)
    # Pool을 이용한 병렬처리
    am_result = am.multiwork_get_game_data(get_log_list)
    # 멀티프로세싱 결과값으로부터 유저 아이디들 분리
    account_ids = []
    for r in am_result[0] :
        r_account_ids = r.popitem()
        if r_account_ids[1] != None :
            account_ids += r_account_ids[1]

    # 멀티프로세싱 결과값들 기존 자료와 결합하여 저장
    new_object = pd.DataFrame(am_result[0])
    old_object = pd.read_parquet('parquets/object.parquet')
    pd.concat([old_object, new_object], axis = 0).reset_index(drop = True).to_parquet('parquets/object.parquet')

    # 유저 아이디들 합친 후 중복값 제거하여 저장
    new_account = pd.DataFrame({'account_id' : account_ids})
    accounts = pd.concat([users, new_account], axis = 0)
    accounts = accounts.drop_duplicates('account_id')
    accounts.reset_index(drop = True).to_parquet("parquets/target_users.parquet", engine = 'pyarrow')

