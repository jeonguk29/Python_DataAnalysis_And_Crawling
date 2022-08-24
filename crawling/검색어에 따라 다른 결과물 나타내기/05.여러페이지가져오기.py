import requests
from bs4 import BeautifulSoup # Beautifulsoup  라이브 러리 불러옴
import pyautogui # 마우스 키보드 매크로 라이브러리 (간단한 입력 창 띄우기)     pip install pyautogui


keyword = pyautogui.prompt("검색어를 입력하세요>>>>")
lastpage = pyautogui.prompt("마지막 페이지번호를 입력해 주세요")


pageNum = 1
# for i in range(시작, 끝, 단계):        1, 10, 2 면    1부터 2씩 들어남 ex 1 3 5 7 9

for i in range(1,int(lastpage) * 10,10):   # 1페이지 부터 3페이지까지  1, 11, 21  
    print(f"{pageNum} 페이지 입니다.======================================")

    # URL 파라미터는 키와 벨류 값으로 되어있는데 크롤링 할때 이부분이 매우 중요함 쿼리 부분 이 바뀌면 검색명이 달라지는 것임 
    response = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}")
    html = response.text  # 웹사이트 전체 html 코드
    soup = BeautifulSoup(html,'html.parser')
    links = soup.select(".news_tit")  # 기사 10개 가져올거라 select 로 찾아야함 안에 css 선택자 적어주면 됨 
    for link in links:
        title = link.text   # 태그 안에 텍스트 요소를 가져온다 
        url = link.attrs['href'] # href 의 속성 값을 가져온다
        print(title,url)
    
    pageNum = pageNum + 1
