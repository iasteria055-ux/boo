import requests
from bs4 import BeautifulSoup

# [수정 필요] 아까 배포했던 그 긴 구글 앱스 스크립트 주소를 여기에 넣으세요!
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxwe7MV1EcPA5xG1_qY19oJtTmPHZnPYCYUv-dusHX-1wASJhVBLEDF4avCrJPN_pny/exec"

def get_data():
    users = {} # {닉네임: {post, comment, recommend, donation, quest}}

    # 1. 게시판 활동 데이터 (닉네임, 게시글)
    res = requests.get("https://ygosu.com/board/pan_boo")
    soup = BeautifulSoup(res.text, 'html.parser')
    for row in soup.select('.bd_list tbody tr'):
        nick = row.select_one('.name a')
        if nick:
            name = nick.text.strip()
            if name not in users: users[name] = {'name': name, 'post': 0, 'comment': 0, 'recommend': 0, 'donation': 0, 'quest': 0}
            users[name]['post'] += 1

    # 2. 기부/일퀘 데이터 (창고) - 예시 구조입니다 (실제 테이블 구조에 맞춰 수정 필요)
    res_min = requests.get("https://ygosu.com/board/pan_boo/?mode=mineral_storage")
    soup_min = BeautifulSoup(res_min.text, 'html.parser')
    # 아래는 예시이며, 실제 창고 테이블의 tr/td 구조에 따라 select 경로 수정 필요
    for row in soup_min.select('table tr'): 
        cols = row.select('td')
        if len(cols) > 2:
            name = cols[0].text.strip()
            if name in users:
                users[name]['donation'] = int(cols[1].text.replace(',',''))
                users[name]['quest'] = int(cols[2].text.replace(',',''))

    return list(users.values())

def push_to_sheet(data):
    # 구글 앱스 스크립트로 데이터 전송
    try:
        response = requests.post(GOOGLE_SHEET_URL, json=data)
        print("전송 성공:", response.status_code)
    except Exception as e:
        print("전송 실패:", e)

if __name__ == "__main__":
    final_data = get_data()
    push_to_sheet(final_data)
