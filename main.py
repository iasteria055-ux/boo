import requests
from bs4 import BeautifulSoup

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxwe7MV1EcPA5xG1_qY19oJtTmPHZnPYCYUv-dusHX-1wASJhVBLEDF4avCrJPN_pny/exec"

def get_data():
    users = {}

    # 1. 활동 데이터 수집
    res = requests.get("https://ygosu.com/board/pan_boo")
    soup = BeautifulSoup(res.text, 'html.parser')
    for row in soup.select('.bd_list tbody tr'):
        nick = row.select_one('.name a')
        vote = row.select_one('.vote')
        comment = row.select_one('.tit span')
        if nick:
            name = nick.text.strip()
            if name not in users: 
                users[name] = {'name': name, 'post': 0, 'comment': 0, 'recommend': 0, 'donation': 0, 'quest': 0}
            users[name]['post'] += 1
            users[name]['recommend'] += int(vote.text) if vote and vote.text.isdigit() else 0
            users[name]['comment'] += int(comment.text.replace('(','').replace(')','').replace('[','').replace(']','')) if comment else 0

    # 2. 기부/일퀘 데이터 수집 (여기가 29번째 줄 근처입니다. 앞의 띄어쓰기를 없애주세요)
    res_min = requests.get("https://ygosu.com/board/pan_boo/?mode=mineral_storage")
    soup_min = BeautifulSoup(res_min.text, 'html.parser')
    for row in soup_min.select('table tr'):
        cols = row.select('td')
        if len(cols) >= 3:
            name = cols[0].text.strip()
            if name in users:
                users[name]['donation'] = int(cols[1].text.replace(',',''))
                users[name]['quest'] = int(cols[2].text.replace(',',''))
    return list(users.values())

def push_to_sheet(data):
    try:
        requests.post(GOOGLE_SHEET_URL, json=data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    final_data = get_data()
    push_to_sheet(final_data)
