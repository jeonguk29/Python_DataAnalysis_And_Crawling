from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 브라우저 생성
browser = webdriver.Chrome("C:\wooogie_kill\chromedriver_win32\chromedriver.exe")

# 웹사이트 열기 
browser.get("https://www.naver.com/")

browser.implicitly_wait(10) # 브라우저 다 로딩 될때 까지 10 초 까지는 기다려줌 


element = browser.find_element(By.CLASS_NAME, 'nav.shop').click()
time.sleep(2)# 2초 기다리고 검색창 찾기 

search = browser.find_element(By.CLASS_NAME, '_searchInput_search_input_QXUFf')
search.click()

# 검색어 입력 
search.send_keys("아이폰 13")
search.send_keys(Keys.ENTER) # 엔터치라는 명령임 


# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY")
# .execute_script 자바 스크립트 명령어 실행 해줌 window.scrollY 스크롤 좌표 를 반환함 

# 무한 스크롤 
while True:
    # 맨 아래로 스크롤을 내린다.
    browser.find_element(By.TAG_NAME,"body").send_keys(Keys.END) # 바티 태그를 찾아서 맨 아래로 내려가는 키를 보냄

    #  스크롤 사이 페이지 로딩 시간 
    time.sleep(1)

    # 스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")

    if after_h == before_h:
        break
    before_h = after_h

# 상품 정보 div 
items = browser.find_elements(By.CLASS_NAME, 'basicList_info_area__17Xyo') # 여러개 일때는 find_elements 리스트 형태로 담아옴 

for item in items:
    
    name = item.find_element(By.CLASS_NAME, 'basicList_title__3P9Q7').text
    try:
    # tip 개수 확인 잘하기 위에 아이템이 40개인데 title 선택하려고 한 클래스 find(컨트롤 + f) 해보니 120 개라면 잘 못 선택한거임 40개라면 40 맞아야함
        price = item.find_element(By.CLASS_NAME, 'price_num__2WUXn').text
    except:
        price = "판매중단" # 판매 중단 된건 위에 클레스가 없어서 오류냄 그래서 직접 값을 넣어 출력해줌
        

    link = item.find_element(By.CLASS_NAME, 'basicList_title__3P9Q7 > a').get_attribute("href")
    # basicList_title__3P9Q7  아래 자식 태그 a에 href 속성 값을 가져옴 

    print(name,price,link)