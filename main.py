import requests
from bs4 import BeautifulSoup

GOOGLE_SHEET_URL = "본인의_구글_앱스_스크립트_주소"

def get_data():
    users = {}
    base_url = "https://ygosu.com/board/pan_boo"
    
    # 1. 게시판 전체 페이지 크롤링
    page = 1
    while True:
        res = requests.get(f"{base_url}?page={page}")
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('.bd_list tbody tr')
        if not rows: break 
        
        for row in rows:
            link = row.select_one('.tit a')
            if not link: continue
            post_url = "https://ygosu.com" + link['href']
            name = row.select_one('.name a').text.strip()
            
            if name not in users:
                users[name] = {'name': name, 'post': 0, 'comment': 0, 'recommend': 0, 'donation': 0, 'quest': 0}
            users[name]['post'] += 1
            
            # 상세 페이지에서 추천인 추출
            try:
                d_res = requests.get(post_url)
                d_soup = BeautifulSoup(d_res.text, 'html.parser')
                for nick in d_soup.select('.view_recommender_detail .nick a'):
                    # 필요시 추천인 데이터도 users에 누적 가능
                    pass
            except: pass
        page += 1

    # 2. 기부/일퀘 창고 전체 페이지 크롤링 (핵심!)
    page_min = 1
    while True:
        res_min = requests.get(f"{base_url}/?mode=mineral_storage&page={page_min}")
        soup_min = BeautifulSoup(res_min.text, 'html.parser')
        rows_min = soup_min.select('table tr')
        # 데이터 행이 없으면(헤더만 있으면) 종료
        if len(rows_min) <= 1: break 
        
        for row in rows_min:
            cols = row.select('td')
            if len(cols) >= 3:
                name = cols[0].text.strip()
                if name not in users:
                    users[name] = {'name': name, 'post': 0, 'comment': 0, 'recommend': 0, 'donation': 0, 'quest': 0}
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
