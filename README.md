## BattleGround Open API활용 웹페이지 개발 

### 프로젝트 개요
- - - 
- 프로젝트 주제 : 배틀그라운드 게임 Open API활용 유저 정보제공 및 전적 정보 제공 기능 홈페이지 제작
- 프로젝트 기간 : 2023.06~2023.08
- 기획의도
  - 유저 전적 정보 및 플레이 스타일 정보 제공
  - 유저의 실제 플레이를 바탕으로 한 무기관련 정보 제공
  - 유저의 착륙지점 및 이동경로 정보 제공

### 기술스택 및 아키텍처 구상도
![image](https://github.com/nbac406/battleGround/assets/125121623/cb9db150-7b87-4e82-91bd-4d86607a7d1b)


### 웹 주요 기능 구상도
- - -
![image](https://github.com/nbac406/battleGround/assets/125121623/bb68a581-e1ea-4edc-87d4-61a08f9fad0c)


### 웹 주요 기능 
<details>
<summary>메인페이지 및 유저 검색 기능</summary>
  
- 유저 검색 기능
- 서버 변경 기능 (KAKAO & STEAM)
- 무기 분석/맵 분석 페이지 이동
- 커뮤니티 워드 클라우드
![image](https://github.com/nbac406/battleGround/assets/125121623/77fbbf80-a021-444f-9f7a-06ed0ab77296)
</details>

<details>
<summary>플레이어 전적 조회</summary>
  
- 검색 유저 닉네임, 선택서버
- 전적 갱신 (Open API 호출)
- 솔로/듀오/스쿼드별 경기 요약
- 유저 무기레벨 top3표시
- 유저 플레이스타일 표시(Kmeans 클러스터링)
- 최근 30일 유저 match이력
![image](https://github.com/nbac406/battleGround/assets/125121623/0b576df5-8f3b-469c-a711-cd218971e29a)
</details>

<details>
<summary>플레이어 전적 조회 - 맵로그</summary>
  
- JavaScripts Leaflet 라이브러리 활용 배틀그라운드 맵 구현
- 유저의 킬 & 데스 로그 (이동경로 및 킬로그 확인)

![image](https://github.com/nbac406/battleGround/assets/125121623/bb6aa045-63b6-4bb2-97de-395c5539cf55)
![image](https://github.com/nbac406/battleGround/assets/125121623/c96ff23a-6c36-4672-a837-c0a58a9b7200)
</details>
