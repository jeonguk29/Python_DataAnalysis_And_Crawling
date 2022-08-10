import requests
from bs4 import BeautifulSoup

# 종목 코드 리스트 
codes = [
    '035420',
    '035720',
    '005930'
]


for code in codes:
    url = f"https://finance.naver.com/item/sise.naver?code={code}"
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    price = soup.select_one("#_nowVal").text  # 현재가는 한개임 select_one      거기에 .text 해서 문자열 내용만 가지고 오면 값 출력됨 
    #print(price) # 91,800

    # 문자열을 숫자로 변환하려면 , 를 없애줘야함 
    price = price.replace(',', '')# 문자열 변환 함수를 이용해 ,를 '' 없애버림 
    print(price)