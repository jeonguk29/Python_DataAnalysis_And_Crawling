import requests
from bs4 import BeautifulSoup # Beautifulsoup  라이브 러리 불러옴



response = requests.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90")
html = response.text  # 웹사이트 전체 html 코드

soup = BeautifulSoup(html,'html.parser')



links = soup.select(".news_tit")  # 기사 10개 가져올거라 select 로 찾아야함 안에 css 선택자 적어주면 됨 
#print(links) # 출력해보면 [] 리스트 형태로 10개가 a태그 10개가 담겨 있음 즉 결과는 리스트 


# 1번 부터 10번까지 기사의 제목과 링크를 가져올수 있음 
for link in links:
    title = link.text   # 태그 안에 텍스트 요소를 가져온다 
    url = link.attrs['href'] # href 의 속성 값을 가져온다
    print(title,url)
