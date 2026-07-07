import requests
from bs4 import BeautifulSoup
import json

# 1. 활동 데이터 채집 (글, 댓글, 추천)
def get_activity_data():
    url = "https://ygosu.com/board/pan_boo"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    users = {}
    # 게시판 리스트에서 닉네임과 활동 데이터 추출 로직
    # (실제 와이고수 HTML 클래스에 따라 수정이 필요할 수 있습니다)
    rows = soup.select('.list_table tbody tr') 
    for row in rows:
        nick = row.select_one('.nickname').text.strip()
        # 글, 댓글, 추천 로직 추가...
        if nick not in users:
            users[nick] = {'post': 0, 'comment': 0, 'recommend': 0}
        users[nick]['post'] += 1
    return users

# 2. 기부/일퀘 데이터 채집 (창고)
def get_mineral_data():
    url = "https://ygosu.com/board/pan_boo/?mode=mineral_storage"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    minerals = {}
    # 창고 테이블에서 닉네임, 기부량, 일퀘량 추출 로직
    # ...
    return minerals

# 3. 데이터 병합 및 구글 시트로 보내기
def send_to_google_sheet(data):
    # 구글 앱스 스크립트 웹 앱 주소로 데이터를 POST로 보냅니다.
    # (인증서 필요 없는 초간단 방식!)
    url = "당신이_받은_구글_앱스_스크립트_URL"
    requests.post(url, json=data)

if __name__ == "__main__":
    # 데이터 수집 -> 병합 -> 전송
    print("크롤링 시작...")
    # ...
