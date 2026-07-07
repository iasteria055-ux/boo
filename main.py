import requests
from bs4 import BeautifulSoup

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxwe7MV1EcPA5xG1_qY19oJtTmPHZnPYCYUv-dusHX-1wASJhVBLEDF4avCrJPN_pny/exec"

def get_data():
    users = {}
    base_url = "https://ygosu.com/board/pan_boo"
    
    # 1. 게시판 활동 데이터 (모든 페이지)
    page = 1
    while True:
        res = requests.get(f"{base_url}?page={page}")
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('.bd_list tbody tr')
        if not rows: break 
        
        for row in rows:
            nick_tag = row.select_one('.name a')
            if not nick_tag: continue
            name = nick_tag.text.strip()
            if name not in users:
                users[name] = {'name': name, 'post': 0, 'comment': 0, 'recommend': 0, 'donation': 0, 'quest': 0}
            users[name]['post'] += 1
            
            vote = row.select_one('.vote')
            comment = row.select_one('.tit span')
            if vote and vote.text.isdigit(): users[name]['recommend'] += int(vote.text)
            if comment:
                c = comment.text.replace('(','').replace(')','').replace('[','').replace(']','').strip()
                if c.isdigit(): users[name]['comment'] += int(c)
        page += 1
    
    # 2. 기부/일퀘 데이터 (모든 페이지)
    page_min = 1
    while True:
        res_min = requests.get(f"{base_url}/?mode=mineral_storage&page={page_min}")
        soup_min = BeautifulSoup(res_min.text, 'html.parser')
        rows_min = soup_min.select('table tr')
        if len(rows_min) <= 1: break # 데이터 행이 없으면 종료
        
        for row in rows_min:
            cols = row.select('td')
            if len(cols) >= 3:
                name = cols[0].text.strip()
                if name in users:
                    users[name]['donation'] += int(cols[1].text.replace(',', ''))
                    users[name]['quest'] += int(cols[2].text.replace(',', ''))
        page_min += 1
    
    return list(users.values())

def push_to_sheet(data):
    try:
        requests.post(GOOGLE_SHEET_URL, json=data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    push_to_sheet(get_data())
