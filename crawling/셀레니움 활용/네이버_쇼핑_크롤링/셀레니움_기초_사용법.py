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



