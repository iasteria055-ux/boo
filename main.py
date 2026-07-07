import requests
from bs4 import BeautifulSoup

# [중요] 본인의 구글 앱스 스크립트 주소로 꼭 교체하세요!
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxwe7MV1EcPA5xG1_qY19oJtTmPHZnPYCYUv-dusHX-1wASJhVBLEDF4avCrJPN_pny/exec"

def get_data():
    users = {}

    # 1. 게시판 활동 데이터 (닉네임, 글, 댓글, 추천)
    res = requests.get("https://ygosu.com/board/pan_boo")
    soup = BeautifulSoup(res.text, 'html.parser')
    
    for row in soup.select('.bd_list tbody tr'):
        nick_tag = row.select_one('.name a')
        vote_tag = row.select_one('.vote')
        comment_tag = row.select_one('.tit span')
        
        if nick_tag:
            name = nick_tag.text.strip()
            if name not in users: 
                users[name] = {'name': name, 'post': 0, 'comment': 0, 'recommend': 0, 'donation': 0, 'quest': 0}
            
            users[name]['post'] += 1
            
            # 추천수 처리 (숫자만 추출)
            if vote_tag and vote_tag.text.isdigit():
                users[name]['recommend'] += int(vote_tag.text)
            
            # 댓글수 처리 (괄호 제거 후 숫자만 추출)
            if comment_tag:
                raw_comment = comment_tag.text.replace('(','').replace(')','').replace('[','').replace(']','').strip()
                if raw_comment.isdigit():
                    users[name]['comment'] += int(raw_comment)

    # 2. 기부/일퀘 데이터 (창고)
    try:
        res_min = requests.get("https://ygosu.com/board/pan_boo/?mode=mineral_storage")
        soup_min = BeautifulSoup(res_min.text, 'html.parser')
        for row in soup_min.select('table tr'):
            cols = row.select('td')
            if len(cols) >= 3:
                name = cols[0].text.strip()
                if name in users:
                    # 콤마 제거 후 숫자로 변환
                    users[name]['donation'] = int(cols[1].text.replace(',',''))
                    users[name]['quest'] = int(cols[2].text.replace(',',''))
    except Exception as e:
        print("창고 데이터 수집 실패:", e)

    return list(users.values())

def push_to_sheet(data):
    try:
        response = requests.post(GOOGLE_SHEET_URL, json=data)
        print("전송 성공:", response.status_code)
    except Exception as e:
        print("전송 실패:", e)

if __name__ == "__main__":
    final_data = get_data()
    push_to_sheet(final_data)
