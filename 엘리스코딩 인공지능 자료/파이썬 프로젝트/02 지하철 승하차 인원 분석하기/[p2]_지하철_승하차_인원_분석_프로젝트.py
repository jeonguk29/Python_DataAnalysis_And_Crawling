#!/usr/bin/env python
# coding: utf-8

# # [Project 2] 지하철 승하차 인원 분석

# ---

# ## 프로젝트 목표

# - 승차 또는 하차 시 해당 시간, 해당 역의 승객 수를 확인하기 위해 **개찰구 통과 승객 수** 데이터와 **지하철 위치좌표** 데이터를 활용
# - 탐색적 데이터 분석을 수행하기 위한 데이터 정제, 특성 엔지니어링, 시각화 방법 학습

# ---

# ## 프로젝트 목차
# 1. **데이터 읽기:** 승하차 인원 정보 데이터를 불러오고 DataFrame 구조를 확인<br>
#     1.1. 데이터 불러오기<br>
#     1.2. 데이터 확인하기<br>
# <br>
# 2. **데이터 정제:** 데이터 확인 후 형 변환 및 이상치 데이터 처리<br>
#     2.1. 2021년 6월 승하차 인원만 추출<br>
# <br>
# 3. **데이터 시각화:** 각 변수별로 추가적인 정제 또는 feature engineering 과정을 거치고 시각화를 총해 데이터 특성 파악<br>
#     3.1. 호선 별 이용객 수 출력<br>
#     3.2. 특정 호선에서 역별 평균 승하차 인원 데이터 추출<br>
#     3.3. 평균 승하차 인원 수 내림차순으로 막대그래프 출력<br>
#     3.4. 특정 호선의 혼잡 정도와 위치좌표 데이터 병합<br>
#     3.5. 특정 호선의 혼잡 정도를 지도에 출력<br>

# ---

# ## 데이터 출처
# - 서울시 지하철 호선별 역별 승하차 인원 정보 데이터: http://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do

# ---

# ## 프로젝트 개요

# 코로나 시국에 익숙해졌다고는 하지만 가끔 밖으로 나갈 때 사람 많은 곳은 피하고 싶은 생각에 어떤 장소를 피해야 하는지 알아보고 싶을 때가 있을 겁니다. 지하철 이용 승객 수를 확인해보면 혼잡도가 높은 지역을 확인해볼 수 있을 것 같습니다.
# 
# 이번 프로젝트에서는 서울 열린 데이터 광장에서 제공하는 `서울시 지하철 호선별 역별 승하차 인원 정보` 데이터를 분석하고 `지하철 역 위치 좌표` 데이터를 활용해 특정 호선에서 어떤 역이 가장 혼잡한지 직관적으로 확인해봅시다.

# ---

#  

# ## 1. 데이터 읽기

# 필요한 패키지 설치 및 `import`한 후 `pandas`를 사용하여 데이터를 읽고 어떠한 데이터가 저장되어 있는지 확인합니다.

# ### 1.1. 데이터 불러오기

# In[1]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt # matplotlib 라이브러리는 그래프 데이터 시각화를 지원
# 이것은 라이브러리에서 pyplot 모듈을 불러오고 약자를 plt라고 사용함 


# 먼저, 서울시 지하철 호선별 역별 승하차 인원 정보 데이터를 불러와 `metro_all`에 저장합니다.

# In[2]:


# pd.read_csv를 통하여 승하차 인원 정보 데이터를 데이터프레임 형태로 읽어옵니다.
metro_all = pd.read_csv("./data/서울시 지하철 호선별 역별 시간대별 승하차 인원 정보_20210705.csv", encoding = 'cp949')
# 판다스 모듈의 함수를 이용 csv파일에 한글이 있을때 encoding = 'cp949' 주로 이렇게 인코딩 하라고 알려줌


# In[3]:


# 승하차 인원 정보 상위 5개 데이터를 출력합니다.
metro_all.head()


# In[4]:


# 승하차 인원 정보 데이터프레임 정보를 요약하여 출력합니다. 
metro_all.info() # 총 52가지 정보가 들어있는걸 알수 있음 
# 전체 45338개 데이터가 null값또한 없음
# 호선명 지하철역 빼고 나머지는 모두 int형임 
# 이 데이터 타입을 미리알면 나중에 데이터 분석시 실수 안함


#  

# ### 1.2. 데이터 확인하기

# 불러온 두 데이터프레임의 특정 컬럼 데이터를 **중복없이 오름차순 정렬하여** 확인해봅시다.

# In[5]:


# metro_all DataFrame 사용월 데이터 확인
sorted(list(set(metro_all['사용월']))) #set함수로 아까 6월 중복된 데이터가 많았는데 이와 같은걸 다 제거해줌 
# 그리고 리스트형태로 변환하기 위해 list 함수와 오름차순을 위해 soted함수 사용함 


# In[6]:


# metro_all DataFrame 호선명 데이터 확인
sorted(list(set(metro_all['호선명'])))


# In[7]:


# DataFrame 지하철역 데이터 확인
sorted(list(set(metro_all['지하철역'])))


# In[10]:


# DataFrame 지하철역 데이터 개수 확인
"""
len(list(set(metro_all['사용월']))) 78
2015년 1월부터 2021년 6월까지는 총 78개월임 
치하철역 개수는 579 그리고 각호선 별로 환승 가능한곳도 있음 
그호선을 중첩하지않고 카운트하면 608개가 됨 
그러니 78 * 608 하면 47424 개가 되는데 2015년부터 새로 생긴역도 있을거라
데이터가 일부 빠진것을 고려하면 45338 개가 되는 것임 
이렇게 데이터 프레임을 볼때 전체 데이터 크기가 나타내는것이 무엇인가 이런것들을
미리 확인해두고 시작하면 좋음 
"""
len(list(set(metro_all['지하철역']))) # 중복제거후 몇개나 있는가  


# --- 

# ## 2. 데이터 정제

# 데이터를 확인해보니 2015년 1월부터 2021년 6월까지 수집된 데이터인 것을 알 수 있습니다.
# 
# 이번 프로젝트에서는 **가장 최근 한달간 수집된 데이터**를 기준으로 특정 호선에서 어떤 역이 가장 혼잡한지 확인하고자 합니다.

# ### 2.1. 2021년 6월 승하차 인원만 추출

# 수집된 데이터 중 가장 최근인 6월에 수집한 데이터만 추출하고 불필요한 컬럼을 제거해봅시다.

# In[11]:


# 2021년 6월 총 승객수만 추출
metro_recent = metro_all[metro_all['사용월']==202106]
metro_recent


# In[12]:


# 불필요한 작업일자 컬럼 제거 (용량 줄이고 계산 빠르게 하기위해서 )
metro_recent = metro_recent.drop(columns={'작업일자'})
metro_recent #이제 52개 컬럼이 아니라 51개 컬림이 나옴 


# ---

# ## 3. 데이터 시각화

# 2021년 6월 데이터만 추출한 `metro_recent`를 활용하여 다양한 데이터 시각화 및 혼잡도 분석을 진행해봅시다.

# ### 3.1. 호선 별 이용객 수 출력

# 추출한 `metro_recent` 데이터를 활용해 이용객 수가 가장 많은 호선 순으로 막대그래프를 출력해 보겠습니다.

# In[13]:


import matplotlib.font_manager as fm # 글씨체 이쁘게 하기위한 

font_dirs = ['/usr/share/fonts/truetype/nanum', ] # 나눔 폰트 사용 
font_files = fm.findSystemFonts(fontpaths=font_dirs)


for font_file in font_files:
    fm.fontManager.addfont(font_file) 


# In[14]:


metro_line = metro_recent.groupby(['호선명']).mean().reset_index()
# 그룹바이는 호선별로 하고 민함수를 이용해 평균을 구함  reset_index() 함수를 이용해 
# 인덱스를 리셋해놓고 이따가 다시 셋팅 하겠음 지금 보면 3가지 함수가 연결되어있는데 
# 이런식으로. 으로 연결할수 있는걸 알아두자 

metro_line = metro_line.drop(columns='사용월').set_index('호선명')
# 6월만 쓰니까 사용월을 지움 그리고 나서 이때 인덱스 이름을 호선명으로 다시 셋팅 


metro_line = metro_line.mean(axis=1).sort_values(ascending=False)
 # 아까 시간대별 값을 평균으로 계산한다고함 가로로 계산 할거니까 axis 축은 1
# 정렬할건데 ascending=False 가장 큰값부터 내림차순으로 하겠음 
    
plt.figure(figsize=(20,10))
plt.rc('font', family="NanumBarunGothic") # 폰트설정 
plt.rcParams['axes.unicode_minus'] = False # .rcParams 변수 조정 함수 [] 안에 axes 축에 마이너스 부호가 
#있을때 깨져 보이는걸 방지함 

metro_line.plot(kind=('bar')) # 이때 그릴때 바에 종휴는 바를 하겠다는 뜻 
plt.show()


# ### 3.2. 특정 호선에서 역별 평균 승하차 인원 데이터 추출

# 다양한 호선에서 역별 평균 승하차 인원이 많은 역은 어디일까요? 이용객이 가장 많은 2호선 기준으로 확인해봅시다.

# In[15]:


line = '6호선'
metro_st = metro_recent.groupby(['호선명','지하철역']).mean().reset_index()
# 호선명과 지하철역 기준으로 그룹바이를 하고 민 함수로 평균값을 계산하고 인덱스를 리셋하겠음 
metro_st_line2 = metro_st[metro_st['호선명']==line] #2호선 값만 추출 
metro_st_line2


# In[16]:


# 승차 인원 컬럼만 추출
metro_get_on = pd.DataFrame()
metro_get_on['지하철역'] = metro_st_line2['지하철역']
# 위에 실핸한 표를 보면 홀수 인덱스 별로 5, 7, 9 자리에 승차인원이 있음 그리고 오른쪽에는 하차 인원이 
#있음 하차인원은 4 6 8  이렇게 짝수 인덱스에 있음
# 주의 할건 0,1,2 인덱스는 승차인원도 하차 인원도 아니니까  이 새개를 제외하고 for문 사용할것임
"""
맨오른쪽 보면 03 ~04 하차인원이 마지막 컬럼에 위치함 맨아래에 51개에 컬럼이 있다고함 
그말은 0번째 인덱스를 고려해서 마지막 하차인원이 인덱스 50이 되는 것임 그러면 3부터 49까지 
홀수 개수는 24개 짝수도 24개 즉 승차 하차 컬럼이 각각 24개 인것을 확인 
"""
for i in range(int((len(metro_recent.columns)-3)/2)): 
    metro_get_on[metro_st_line2.columns[3+2*i]] = metro_st_line2[metro_st_line2.columns[3+2*i]]
metro_get_on = metro_get_on.set_index('지하철역')
metro_get_on


# In[17]:


# 하차 인원 컬럼만 추출
metro_get_off = pd.DataFrame()
metro_get_off['지하철역'] = metro_st_line2['지하철역']
for i in range(int((len(metro_recent.columns)-3)/2)):
    metro_get_off[metro_st_line2.columns[4+2*i]] = metro_st_line2[metro_st_line2.columns[4+2*i]]
metro_get_off = metro_get_off.set_index('지하철역')
metro_get_off


# In[18]:


# 역 별 평균 승하차 인원을 구한 후 정수로 형 변환하여 데이터프레임으로 저장
df = pd.DataFrame(index = metro_st_line2['지하철역'])
df['평균 승차 인원 수'] = metro_get_on.mean(axis=1).astype(int) # 민함수로 평균냄 axis=1)가로로 계산 평균이라 소수점이 나올테니 인트형으로 해줌  
df['평균 하차 인원 수'] = metro_get_off.mean(axis=1).astype(int)
df


# ### 3.3. 평균 승하차 인원 수 내림차순으로 막대그래프 출력

# 2호선 기준 6월 한 달간 **강남 > 잠실 > 신림 > 구로디지털단지 > 홍대입구 > 선릉** 순으로 평균 승차 인원이 많았습니다.

# In[19]:


# 승차 인원 수 Top10 
top10_on = df.sort_values(by='평균 승차 인원 수', ascending=False).head(10)
# 평균 승차 인원 수 기준으로 정렬하고 내림차순으로 False값주고 탑 10만 골라냄 
plt.figure(figsize=(20,10))
plt.rc('font', family="NanumBarunGothic")
plt.rcParams['axes.unicode_minus'] = False

plt.bar(top10_on.index, top10_on['평균 승차 인원 수']) # bar함수 안에는 가로축,세로축 값 순서임 
for x, y in enumerate(list(top10_on['평균 승차 인원 수'])): # enumerate 열거하다라는 뜻의 함수 
    if x == 0:   # 내림차순으로 탑10골랐는데 그러면 0번째 인덱스는 가장 숫자가 큰것일것 
        plt.annotate(y, (x-0.15, y), color = 'red') # 가장큰 값만 특정 효과를 줌 
    else:
        plt.annotate(y, (x-0.15, y))

plt.title('2021년 6월 평균 승차 인원 수 Top10')
plt.show()


# 평균 하차 인원은 거의 동일하게 **강남 > 잠실 > 신림 > 구로디지털단지 > 홍대입구 > 역삼** 순으로 많았습니다.

# In[20]:


# 하차 인원 수 Top10
top10_off = df.sort_values(by='평균 하차 인원 수', ascending=False).head(10)

plt.figure(figsize=(20,10))
plt.rc('font', family="NanumBarunGothic")
plt.rcParams['axes.unicode_minus'] = False

plt.bar(top10_off.index, top10_off['평균 하차 인원 수'])
for x, y in enumerate(list(top10_off['평균 하차 인원 수'])):
    if x == 0:
        plt.annotate(y, (x-0.15, y), color = 'red')
    else:
        plt.annotate(y, (x-0.15, y))

plt.title('2021년 6월 평균 하차 인원 수 Top10')
plt.show()


# **퀴즈1. 6호선의 지하철 역 중에서 승차 인원수가 가장 많은 역명을 구하세요.**

# In[21]:


# 3.2.의 첫 번째 셀에서 line값만 수정한 후 


# 3.2.와 3.3. 코드를 순서대로 다시 실행해보면 답을 구할 수 있습니다.

top1_on = df.sort_values(by='평균 승차 인원 수', ascending=False).head(1)
top1_on.index[0]


# In[22]:


# 6호선 지하철 역 중 승차 인원 수가 가장 많은 역명을 quiz_1 변수에 저장합니다.
# '~~역'에서 역을 제외한 ~~을 문자형으로 저장합니다.
quiz_1 = top1_on.index[0]
quiz_1


# ### 3.4. 특정 호선의 혼잡 정도와 위치좌표 데이터 병합

# 특정 호선의 지하철 역 마다 지도에 정보를 출력하기 위해서는 각 위치의 좌표정보가 필요합니다.
# 
# 이를 해결하기 위해 카카오 API를 활용하여 csv 파일로 만들어두었습니다.
# 
# 출처: <br>
# https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword<br>
# https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord

# In[23]:


# 지하철 역별 위치좌표에 대한 데이터를 불러옵니다.
subway_location = pd.read_csv('./data/지하철 역 위치 좌표.csv') # 위도 경도를 가지고 있음
subway_location


# 먼저 특정 호선의 역별 평균 승하차 인원 수와 지하철 역별 위치좌표 데이터를 병합하여 데이터프레임을 생성해봅시다.

# In[24]:


# 특정 호선의 역별 평균 승하차 인원 수와 지하철 역 위치 좌표를 데이터프레임으로 반환하는 함수입니다.
def get_nums_and_location(line, metro_st):
    # 이럴땐 호선별 지하철역별로 분석 할수 있도록 새로운 함수를 만들면 편함 
    
    # 특정 호선의 데이터만 추출합니다.
    metro_line_n = metro_st[metro_st['호선명']==line] # 호선명이 라인인것만 추출 
    
    # 승차 인원 컬럼만 추출합니다.
    metro_get_on = pd.DataFrame()
    metro_get_on['지하철역'] = metro_line_n['지하철역'] # metro_line_n만다르고 나머지 위에서 설명함
    for i in range(int((len(metro_recent.columns)-3)/2)):
        metro_get_on[metro_line_n.columns[3+2*i]] = metro_line_n[metro_line_n.columns[3+2*i]]
    metro_get_on = metro_get_on.set_index('지하철역')
    
    # 하차 인원 컬럼만 추출합니다.
    metro_get_off = pd.DataFrame()
    metro_get_off['지하철역'] = metro_line_n['지하철역']  # metro_line_n만다르고 나머지 위에서 설명함
    for i in range(int((len(metro_recent.columns)-3)/2)):
        metro_get_off[metro_line_n.columns[4+2*i]] = metro_line_n[metro_line_n.columns[4+2*i]]
    metro_get_off = metro_get_off.set_index('지하철역')
    
    # 역 별 평균 승하차 인원을 구한 후 정수로 형 변환하여 데이터프레임으로 저장합니다.
    df = pd.DataFrame(index = metro_line_n['지하철역'])   # metro_line_n만다르고 나머지 위에서 설명함
    df['평균 승차 인원 수'] = metro_get_on.mean(axis=1).astype(int) 
    df['평균 하차 인원 수'] = metro_get_off.mean(axis=1).astype(int)
    
    # 지하철역 명 동일하도록 설정합니다.
    temp = []       # 우리가 크게 두개에 데이터 프레임을 병합하는 거잖아요 
    """
     첫번째는 지하철역에 승하차 인원이고 두번째는 지하철역에 위도 경도 위치입니다 
    그런데 이 지하철이름이 좀 다르게 구성되어 있어요 첫번째 데이터에서는 구의 (광진구청)
    두번째 데이터에서는 구의 라고만 적혀있음 컴퓨터는 이걸 구분 못하기 때문에 첫번째 데이터에
    괄호 앞 부분'('까지만 잘라서 통일 하겠음 
    """
    
    df = df.reset_index() #인덱스를 초기화 해서 시작하겠음 
    for name in df['지하철역']:   # 지하철역 컬럼 
        temp.append(name.split('(')[0]+'역')   # temp에 추가함  name.split 즉 나누는데 괄호앞 즉 '(' 이거 말하는거임
          # 즉 괄호 앞기준으로 0번째에 위치한것을 불러오겠다는 듯임 그뒤에 '역'이라고 이름 붙임 
    df['지하철역'] = temp # 이렇게 구한 temp값을  앞데이터 프레임 지하철역 컬럼에 넣으면 됨 
    
    # 지하철역 명을 기준으로 두 데이터프레임 병합합니다.  
    df = df.merge(subway_location, left_on='지하철역', right_on='지하철역')
    
    # merge 함수를 써서 두번째 데이터 프래임 subway_location 병합할 것임 왼쪽 오른쪽 둘다 기준 컬럼이 지하철역임

    return df


# In[25]:


get_nums_and_location('6호선', metro_st) # 함수에 변수를 넣어봄 


# ### 3.5. 특정 호선의 혼잡 정도를 지도에 출력

# 지도를 출력하기 위한 라이브러리로 folium을 사용해 봅시다.

# In[26]:


import folium

# 특정 위도, 경도 중심으로 하는 OpenStreetMap을 출력
map_osm = folium.Map(location = [37.529622, 126.984307], zoom_start=12) #이전프로젝트에 해봤음
map_osm


# 이제 특정 호선의 역별 평균 승차 인원 수를 원형마커를 통해 지도에 출력해봅시다.

# In[27]:


# 특정 호선의 역별 평균 승하차 인원 수와 위치좌표 데이터만 추출합니다.
rail = '6호선'
df = get_nums_and_location(rail, metro_st)

# 서울의 중심에 위치하는 명동역의 위도와 경도를 중심으로 지도 출력합니다.
latitude = subway_location[subway_location['지하철역']=='명동역']['x좌표']
longitude = subway_location[subway_location['지하철역']=='명동역']['y좌표']
map_osm = folium.Map(location = [latitude, longitude], zoom_start = 12)

# 각 지하철 역의 위치별로 원형마커를 지도에 추가합니다.
for i in df.index:
    marker = folium.CircleMarker([df['x좌표'][i],df['y좌표'][i]],    #
                        radius = (df['평균 승차 인원 수'][i]+1)/3000, #인원 수가 0일 때 계산오류 보정 ( +1 해줌으로 )
                                 # 원형 마커 범위를 승하차 인원수 정도에 따라 크게 만들것임 
                        popup = [df['지하철역'][i],df['평균 승차 인원 수'][i]],  # 팝업을통해 가시적으로 보여줌 
                        color = 'blue', 
                        fill_color = 'blue')
    marker.add_to(map_osm) # 원형 마커 지도에 추가 

map_osm


# **퀴즈2. 강남역의 x좌표(위도)를 구하세요.**

# In[34]:


# get_nums_and_location() 함수를 활용하면 쉽게 구할 수 있습니다.
# 강남역은 2호선이기 때문에 df = get_nums_and_location('2호선', metro_st)으로 데이터프레임을 추출합니다.
# df[df['지하철역']=='강남역']['x좌표']을 통해 컬럼 '지하철역'이 '강남역'인 행을 추출하고 'x좌표'값을 구해보세요.

df = get_nums_and_location('2호선', metro_st) 
x = df[df['지하철역']=='강남역']['x좌표']
x[0]


# In[36]:


# float형으로 좌표값만 저장합니다. 예시: 37.123456
quiz_2 = x[0]


# ---

# ## 제출하기

# 퀴즈 1번과 2번을 수행 후, 아래 코드를 실행하면 `quiz_1 ~ 2` 변수가 저장된 csv 파일을 제작하여 채점을 받을 수 있습니다.
# 
# **아래 코드를 수정하면 채점이 불가능 합니다.**

# In[37]:


d = {'quiz_1': [quiz_1], 'quiz_2': [quiz_2]}
df_quiz = pd.DataFrame(data=d)
df_quiz.to_csv("submission.csv",index=False)


# In[38]:


# 채점을 수행하기 위하여 로그인
import sys
sys.path.append('vendor')
from elice_challenge import check_score, upload


# In[39]:


# 제출 파일 업로드
await upload()


# In[40]:


# 채점 수행
await check_score()

