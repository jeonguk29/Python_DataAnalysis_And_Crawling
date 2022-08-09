import requests
from bs4 import BeautifulSoup # Beautifulsoup  라이브 러리 불러옴


# 네이버 서버에 대화를 시도 
response = requests.get("https://www.naver.com/") 

# 네이버 에서 html을 줌 
html = response.text


# html 번역 선생님으로 수프 만듬  
soup = BeautifulSoup(html,'html.parser')  # html 소스와 html점검 프로그램 넣어주면 태그 추출 같은게 가능


# id 값이 NM_set_home_btn인 놈 한개를 찾아냄 
word = soup.select_one("#NM_set_home_btn") # select는 여라개 태그 선택, select_one 은 한개 태그 선택 
# 중요한거 클래스면 앞에. id면 # 붙여줘야함 css선택자라고 함
# print(word)   이렇게만 하면 태그 전체를 가져옴 

# 택스트 요소만 추력 
print(word.text)  # .text 붙여주면 text 부분 글 부분만 가져옴 