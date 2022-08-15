from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# pip install webdriver_manager  설치후 
# 크롬 드라이버 자동 업데이트 
from webdriver_manager.chrome import ChromeDriverManager


# 너무 빨리 입력되서 로봇인거 같다고 함 그래서 3개 라이브러리 가져올 필요 있음
import time
import pyautogui
import pyperclip


# 브라우저 꺼짐 방지 
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 이놈은 크롬 드라이버 매니저 라는 놈을 통해서 자동으로 크롬 드라이버를 최신으로 설치하고 가져오게 하는 것임
service = Service(executable_path=ChromeDriverManager().install())
# 웹브라우저 가져올건데 위에서 정의한 최신버전으로 가져와라 
driver = webdriver.Chrome(service=service, options=chrome_options)



# 웹페이지 해당 주소 이동
driver.implicitly_wait(5) # 웹페이지가 로딩될때 까지 5초 기다려줌
driver.maximize_window() # 화면 최대화 

driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")


# 아이디 입력창 
id =  driver.find_element(By.CSS_SELECTOR, "#id")
id.click()
#id.send_keys("jeonguk29")
pyperclip.copy("아이디") # 클립보드 복사후
pyautogui.hotkey("ctrl","v") # 컨트롤 v 하면 로봇인거 피할수 있음 
time.sleep(2)

# 아이디 입력창 
pw =  driver.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
#pw.send_keys("비번")

pyperclip.copy("비번") # 클립보드 복사후
pyautogui.hotkey("ctrl","v") # 컨트롤 v 하면 로봇인거 피할수 있음 
time.sleep(2)

# 로그인 버튼 클릭
login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
login_btn.click()