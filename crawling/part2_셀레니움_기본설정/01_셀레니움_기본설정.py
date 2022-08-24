from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# pip install webdriver_manager  설치후 
# 크롬 드라이버 자동 업데이트 
from webdriver_manager.chrome import ChromeDriverManager



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
driver.get("https://www.naver.com/")
