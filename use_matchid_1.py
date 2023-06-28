import requests
import pymysql
import time
import json
import py7zr
import os
import datetime



con = pymysql.connect(
    host = '3.37.122.17', 
    user = 'team', 
    password = '123', 
    port = 3306, 
    database = 'battleGround')

cur = con.cursor()
cur.execute('USE battleGround;')
con.commit()

# header 설정
author1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMjg0ZDBjMC1lMGQ5LTAxM2ItNGVlNS0wMjJlZGE2MTJmNmMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NDI0NjU0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFwaTEifQ.FoLqbKF83KfdOo42OvkoLlswFp78ftcXFeP9akV8R4g'
author2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiNjA3NjExMC1lMThkLTAxM2ItNGVlOC0wMjJlZGE2MTJmNmMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTAyMjM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImZvcl9hZGRfcmVxdWVzIn0._ZnA0opuvzWy8ONFTOO6wq5WHA90lw3aQD9SsABmM_M'
author3 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmYzA1NjA5MC1lMTlkLTAxM2ItYWIwZC00YWQ1NTRmZjEzNWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTA5MjI4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii02N2NjOWEzZC1jNzk5LTQ5MjgtYWZhOS03ZGExZWRiMjA0ZmQifQ.2NVhbJS3pjOp-SJLRH_pOYf3p3Zn_hAh6fxzO5-3NN8'
#author4 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNDM1Nzc5MC1lMTllLTAxM2ItNDRhYi01NmE0MmY0YzFkNGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTA5MjY4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii01MWYxYjNhNC05YTJkLTQ1MzAtOWIyMy03YjU4YzI5NTZmZTIifQ.XxqN69vTIwkdgRDBxQ2mAHHWkj3Rc3xgsreJhi0KvO4'
#author5 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNDNiMmFkMC1lMGUyLTAxM2ItNWVhYS00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NDI4NTIzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InByb2plY3RfZ2FtZSJ9.rDPrdCT3GOWRp9UEWasFRI7EuE_HlnDyvGq_eENzzak' # 재규
#author6 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3YjViOWQ2MC1lMWE0LTAxM2ItNDRhZC01NmE0MmY0YzFkNGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEyMDE4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii02ODhiY2QyNi0yZDdiLTRlNDMtYTE0NC0yOWUwNGRiOTNiMmEifQ.I2rwkm5XYxyjktRKvFJNb4jTRO28FjHzD7JEK8C-dGo' # 재규
#author7 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxZTg2NmE2MC1lMWE1LTAxM2ItYzg2Mi00Mjg1NWU5MDJkNTYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEyMjkyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImRhdGEyIn0.ANcRT57sj3kxDNwvbt_1kHvYRwafpKXXB1juyc1wZ3w' # 혜규
#author8 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwZDJiYjMwMC1lMWE1LTAxM2ItNDRiMC01NmE0MmY0YzFkNGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEyMjYzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05OTQyOTIxMy00YjlkLTQ0MTEtYjI4MS1hOWIwMjBlNjUxYjYifQ.camj7sp5qGdzX11nGeI56nPFNBYqoBzQUwvL0gOXNY0' # 혜규
#author9 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwZTQ5MjFhMC1lMWE4LTAxM2ItNWViMi00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEzNTUzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImRhdGFncm91bmQyIn0.aQ8DgPRZHy3zG9J4RKv3bM76HSDr0g7UK_llq3NQaOs' # 정우형
#author10 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjNjVkNzliMC1kYjMwLTAxM2ItYzgwOS00Mjg1NWU5MDJkNTYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg0ODAyNjE1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImRhdGFncm91bmQifQ.dP4R75BLmPNgHXE8RVak6kmbETnhHuKY-56yD7S1RtI' # 정우형
#author11 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5MmEzOGYzMC1lMWE3LTAxM2ItYzg2NC00Mjg1NWU5MDJkNTYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg1NTEzMzQ2LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1hZjdmNzc5NC1lMzU2LTRjZjUtYTU5Yi0yNDUzNzlkNjg2MjAifQ._JAnysrJ6QNmqw2DmDf0O62HfL77caOlIrsTWerLzFo' # 종범이형
#author12 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTNhYzViMC1kYjQ3LTAxM2ItNWU2YS00MmY3ZTdiY2Q3MWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjg0ODEyMjk3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii04ZWU0NjRkNi1jNjdkLTQyMDEtOGIzNC02N2I4YjUwOWJhYjgifQ.KiEz10CpYXFS2r4SsWq8aizag2oEAy6KtbH0e2TQH7s' # 종범이형

apis = [
    author1,
    author2,
    author3,
    #author4,
    #author5,
    #author6,
    #author7,
    #author8,
    #author9,
    #author10,
    #author11,
    #author12,
]

files = ''.join(os.listdir('/workspace/logs/'))
def process_data(author, matchid) :
    header = {
        "Authorization": author,
        "Accept": "application/vnd.api+json"
    }

    url = f"https://api.pubg.com/shards/kakao/matches/{matchid}"
    
    try :
        r = requests.get(url, headers = header)
    
    except :
        return None
    
    # error 발생 감지
    if 'errors' in list(r.json().keys()) :
        exec = f'DELETE FROM matches WHERE matchId LIKE "{matchid}"'
        cur.execute(exec)
        con.commit()
        print(f'deleted {matchid}')
    else :

        # 어카운트 아이디 추가
        try :
            included = r.json()['included']
            for who in included :
                if who['type'] == 'participant' :
                    player = who['attributes']['stats']['playerId']
                    exec = f'INSERT INTO `user` (`account_id`) values ("{player}");'
                    cur.execute(exec)
            con.commit()


        except :
            print("it's me ", author,' fail the id ', matchid)


        # 매치기록 추가
        try :
            jsonData = json.dumps(r.json())
            exec = f"INSERT INTO `matchRecord` values ('{jsonData}');"
            cur.execute(exec)
            con.commit()


            # 매치 기록 저장 후, 로그데이터 저장
            for x in r.json()['included'] :
                if x['type'] == 'asset' :
                    log_url = x['attributes']['URL']
            log_r = requests.get(log_url)
            logPath = f'logs/{matchid}.txt'
            outputPath = f'logs/{matchid}.7z'
            logFile = open(logPath, 'w')
            logFile.write(str(log_r.json()))
            logFile.close()

            with py7zr.SevenZipFile(outputPath, 'w') as archive:
                archive.write(logPath)

            # 로그 파일 삭제
            os.remove(logPath)
            # 기록된 매치아이디 삭제
            exec = f'DELETE FROM matches WHERE matchId LIKE "{matchid}"'
            cur.execute(exec)
            con.commit()

        except :
            print(type(jsonData))
            print(r)
            print(matchid)
            print('매치기록실패')


# 매치아이디 불러오기
cur.execute('SELECT DISTINCT matchId FROM matches;')
result = cur.fetchall()
per = len(result) // 4
result = result[:per]
# 보조 변수들 정의
start = 1
api_index = 0
len_apis = len(apis)
len_result = len(result)

currentMinute = datetime.datetime.today().minute
tries = 0
maxTries = len(apis) * 10

for match_id in result :
    print(f'1 is {round((start/len_result) * 100, 4)}%')
    
    if tries >= maxTries :
        sleepSecond = 60 - datetime.datetime.today().second
        time.sleep(sleepSecond)
    
    # 분당 제한속도, 
    if currentMinute != datetime.datetime.today().minute :
        currentMinute = datetime.datetime.today().minute
        tries = 0
    
    matchid = match_id[0]
    # 리스트 아웃 인덱싱 방지
    if api_index % len_apis == 0 :
        api_index = 0
    author = apis[api_index]
    
    
    if matchid in files :
        print('passed')
        exec = f'DELETE FROM matches WHERE matchId LIKE "{matchid}"'
        cur.execute(exec)
        con.commit()
        pass
    
    else :
        process_data(author, matchid)
        api_index += 1
        tries += 1
    start += 1