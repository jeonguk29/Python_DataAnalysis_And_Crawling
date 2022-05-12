#!/usr/bin/env python
# coding: utf-8

# # [Project 1] 코로나 데이터 분석

# ---

# ## 프로젝트 목표
# - 서울시 코로나19 확진자 현황 데이터를 분석하여 유의미한 정보 도출
# - 탐색적 데이터 분석을 수행하기 위한 데이터 정제, 특성 엔지니어링, 시각화 방법 학습

# ---

# ## 프로젝트 목차
# 1. **데이터 읽기:** 코로나 데이터를 불러오고 Dataframe 구조를 확인<br>
#     1.1. 데이터 불러오기<br>
# <br> 
# 2. **데이터 정제:** 비어 있는 데이터 또는 쓸모 없는 데이터를 삭제<br>
#     2.1. 비어있는 column 지우기<br>
# <br>
# 3. **데이터 시각화:** 각 변수 별로 추가적인 정제 또는 feature engineering 과정을 거치고 시각화를 통하여 데이터의 특성 파악<br>
#     3.1. 확진일 데이터 전처리하기<br>
#     3.2. 월별 확진자 수 출력<br>
#     3.3. 8월 일별 확진자 수 출력<br>
#     3.4. 지역별 확진자 수 출력<br>
#     3.5. 8월달 지역별 확진자 수 출력<br>
#     3.6. 월별 관악구 확진자 수 출력<br>
#     3.7. 서울 지역에서 확진자를 지도에 출력<br>

# ---

# ## 데이터 출처
# -  https://www.data.go.kr/tcs/dss/selectFileDataDetailView.do?publicDataPk=15063273

# ---

# ## 프로젝트 개요
# 
# 2020년 초에 발생한 코로나19 바이러스는 세계적으로 대유행하였고 이에 대한 많은 분석이 이루어지고 있습니다. 유행 초기엔 이를 분석할 데이터가 충분하지 않았지만 6개월 이상 지난 지금은 다양한 데이터 기관에서 코로나 관련 데이터를 공공으로 제공하고 있습니다.
# 
# 이번 프로젝트에서는 국내 공공데이터 포털에서 제공하는 `서울시 코로나19 확진자 현황` 데이터를 바탕으로 탐색적 데이터 분석을 수행해보겠습니다. 국내 데이터 중 확진자 비율이 제일 높고 사람이 제일 많은 서울시의 데이터를 선정하였으며, 이를 바탕으로 코로나19의 확진 추이 및 환자 특성에 대해서 데이터를 바탕으로 알아봅시다.
# 
# 

# ---

#  

# ## 1. 데이터 읽기

# 필요한 패키지 설치 및 `import`한 후 `pandas`를 사용하여 데이터를 읽고 어떠한 데이터가 저장되어 있는지 확인합니다.

# ### 1.1. 데이터 불러오기

# In[6]:


import numpy as np  #데이터 처리 모듈
import pandas as pd # 데이터 처리 모듈 
import matplotlib.pyplot as plt # 그래프 데이터 시각화 지원 모듈 
import seaborn as sns  # 데이터 시각화 지원 모듈 


# In[8]:


# pd.read_csv를 통하여 dataframe 형태로 읽어옵니다.
corona_all=pd.read_csv("./data/서울시 코로나19 확진자 현황.csv")


# In[10]:


# 상위 5개 데이터를 출력합니다. # 이때 head 함수 사용
corona_all.head()


# In[11]:


# dataframe 정보를 요약하여 출력합니다. #(전체데이터 한눈에 보기 위해 info 함수 사용)
corona_all.info()  # 보면 5748명이 있고 null 값은 개인정보라 안보이는 걸 말함
#여행력 보면 5748 명중 459명은 해외 유입을 말함  디타입 보면 데이터 구성을 알수있음
# 미리 알아두면 뒤에서 실수 안함 


#  

# ---

# ## 2. 데이터 정제

# 데이터를 읽고 확인했다면 결측값(missing data), 이상치(outlier)를 처리하는 데이터 정제 과정을 수행하여 봅시다.

# ### 2.1. 비어있는 column 지우기

# `corona_all.info()` 코드를 통하여 `국적`, `환자정보`, `조치사항` 에 해당하는 데이터가 존재하지 않는 것을 알 수 있습니다.
# 
# `dataframe.drop()`를 사용하여 불필요한 `국적`, `환자정보`, `조치사항` 의 column 데이터를 삭제하고 이 dataframe을 `corona_del_col`에 저장해 봅시다.
# 
# 이렇게 새로운 변수에 정의하고 하는게 좋음 원본에서 삭제하는게 아니라 
# 원본이 다시 필요할때도 있기 때문임 

# In[12]:


# drop 함수를 사용하여 국적, 환자정보, 조치사항 coulmn 데이터를 삭제합니다.
corona_del_col = corona_all.drop(columns = ['국적','환자정보','조치사항'])


# In[13]:


# 정제 처리된 dataframe 정보를 출력합니다. 원본과 비교시 컬럼삭제되었고 데이터 용량도 줄었음 
corona_del_col.info()


# ---

# ## 3. 데이터 시각화

# 데이터 정제를 완료한 `corona_del_col` 데이터를 바탕으로 각 column의 변수별로 어떠한 데이터 분포를 하고 있는지 시각화를 통하여 알아봅시다.

# ### 3.1. 확진일 데이터 전처리하기

# `확진일` 데이터를 간단히 출력해보면 `월.일` 형태의 날짜 형식임을 알 수 있습니다.
# 
# 월별, 일별 분석을 위해서는 문자열 형식의 데이터를 나누어 숫자 형 데이터로 변환해 보겠습니다.

# In[14]:


corona_del_col['확진일']  # 데이터 보니 년표시는 없고 월 일만 있음


# #### `확진일` 데이터를 `month`, `day` 데이터로 나누기

# `확진일`에 저장된 문자열 데이터를 나누어 `month`, `day` column에 int64 형태로 저장해 봅시다.

# In[15]:


# dataframe에 추가하기 전, 임시로 데이터를 저장해 둘 list를 선언합니다.
month = []
day = []

for data in corona_del_col['확진일']:
    # split 함수(나누기함수)를 사용하여 월, 일을 나누어 list에 저장합니다.
    month.append(data.split('.')[0]) # .기준으로 나누겠다 ex 10.21.
    day.append(data.split('.')[1])


# In[16]:


# corona_del_col에 `month`, `day` column을 생성하며 동시에 list에 임시 저장된 데이터를 입력합니다.
corona_del_col['month'] = month
corona_del_col['day'] = day

corona_del_col['month'].astype('int64') # astype 이렇게 데이터 타입을 바꿔줌 
corona_del_col['day'].astype('int64')


#  

# ### 3.2. 월별 확진자 수 출력

# 나누어진 `month`의 데이터를 바탕으로 달별 확진자 수를 막대그래프로 출력해 보겠습니다.

# In[17]:


# 그래프에서 x축의 순서를 정리하기 위하여 order list를 생성합니다.
order = []
for i in range(1,11): # 10월 까지만 있어서 이렇게 해줌 
    order.append(str(i))

order


# In[18]:


# 그래프의 사이즈를 조절합니다.
plt.figure(figsize=(10,5)) # 가로 10 세로 5

# seaborn의 countplot 함수(데이터 개수를 새는 함수)를 사용하여 출력합니다.
# 우리가 따로 개산할 필요없이 원본 데이터에서 바로 카운트 해서 플랏 그려줌 
sns.set(style="darkgrid")
ax = sns.countplot(x="month", data=corona_del_col, palette="Set2", order = order)
# x축은 month 이고 월별로 데이터 카운트 하겠다는 뜻 palette="Set2" 기본 지정된 색상 
# 이용하겠다는 뜻 순서는 order 1부터 10까지 월별 순서로 하겠다
# 그래프 실행해서 버면 y축이 월별 확진자 데이터 수임 


# In[19]:


# 판다스 series의 plot 함수를 사용한 출력 방법도 있습니다.
# 위에서는 월별로 데이터 분석했다면 이번에는 값이 큰거부터 정렬할 수 있습니다 
corona_del_col['month'].value_counts().plot(kind='bar')
# 이 plot 함수를 사용할때는 value_counts() 라는 함수를 사용해서 값의 개수를 확인 할수가 있음
# seaborn 모듈에서는 countplot 카운트와 plot그리기를 한번에 할수 있었는데
# 이 판다스 모듈에서는 카운트를 한번하고 이것을 플랏으로 그리는 두번에 작업을
# 해야함 kind 종류는 바 즉 막대그리프 


# In[20]:


# 위에 value_counts()는 각 데이터를 세어서 내림차순으로 정리하는 함수입니다.
corona_del_col['month'].value_counts()


#  

# ### 3.3. 8월달 일별 확진자 수 출력

# 월별 확진자 수를 출력해보면 알 수 있듯이 8월에 확진자 수가 가장 많았습니다.
# 
# 이번엔 8월 동안 확진자 수가 어떻게 늘었는지 일별 확진자 수를 막대그래프로 출력해 봅시다.

# In[21]:


# 그래프에서 x축의 순서를 정리하기 위하여 order list를 생성합니다.
order2 = []
for i in range(1,32):  # 1일부터 31일까지로 해야함 8월은 31일까지 있어서 
    
    order2.append(str(i))

order2


# In[22]:


# seaborn의 countplot 함수를 사용하여 출력합니다. (월별그래프 그린거랑 거의 비슷함 )
plt.figure(figsize=(20,10))   
sns.set(style="darkgrid")
ax = sns.countplot(x="day", data=corona_del_col[corona_del_col['month'] == '8'], palette="rocket_r", order = order2)
# ax 축 설정  sns.countplot을 이용하겠다 이때 x은 일자가 되고  먼스가 8월인거만 사용 하겠다 
# rocket_r 라는 디폴트 값 사용하고 oder2일자별 리스트 사용 


# #### 퀴즈 1. 8월 평균 일별 확진자 수를 구하세요. (8월 총 확진자/31일)

# In[23]:


corona_del_col[corona_del_col['month'] == '8']['day'].count()/31
# 일별로 평균 내려면 8월에 총확진자에서 31일로 나누면 될것임 => 77.93명
corona_del_col[corona_del_col['month'] == '8']['day'].value_counts().mean()


# In[24]:


# 8월 평균 확진자 수를 구하여 quiz_1 변수에 저장합니다.
# float 형 상수값으로 저장합니다.
quiz_1 =  corona_del_col[corona_del_col['month'] == '8']['day'].value_counts().mean()

quiz_1


#  

# ### 3.4. 지역별 확진자 수 출력

# `지역` 데이터를 간단히 출력해보면 `oo구` 형태의 문자열 데이터임을 알 수 있습니다.

# In[25]:


corona_del_col['지역'] # 확인해버면 5748명에 지역구가 모두 들어가있는걸 볼수 있음 


# 이번에는 지역별로 확진자가 얼마나 있는지 막대그래프로 출력해 봅시다.

# In[26]:


import matplotlib.font_manager as fm #글시체 모듈 불러오겠음 

font_dirs = ['/usr/share/fonts/truetype/nanum', ] # 나눔폰트 이용해보겠음 
font_files = fm.findSystemFonts(fontpaths=font_dirs)
#fm 모듈에 findSystemFonts함수 사용 이때 폰트 paths는 위에서 정한 font_dirs 사용
for font_file in font_files:
    fm.fontManager.addfont(font_file)# addfont함수 사용해서 폰트 추가 


# In[27]:


plt.figure(figsize=(20,10))
# 한글 출력을 위해서 폰트 옵션을 설정합니다.
sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False},  # 이 축에 값이 마이너스면 이 마이너스 부호가 깨져 보여서 
        style='darkgrid')                  # 방지하기위한 코드 
ax = sns.countplot(x="지역", data=corona_del_col, palette="Set2")


#  

# #### 지역 이상치 데이터 처리

# 위의 출력된 데이터를 보면 `종랑구`라는 잘못된 데이터와 `한국`이라는 지역과는 맞지 않는 데이터가 있음을 알 수 있습니다.
# 
# 기존 지역 데이터 특성에 맞도록 `종랑구` -> `중랑구`, `한국` -> `기타`로 데이터를 변경해 봅시다.

# In[28]:


# replace 함수를 사용하여 해당 데이터를 변경합니다.
# 이상치가 처리된 데이터이기에 새로운 Dataframe으로 저장합니다.
corona_out_region = corona_del_col.replace({'종랑구':'중랑구', '한국':'기타'})

# 이렇게 새로운 변수로 지정하는 이유는 원본 데이터 건들지 않기 위함임 
# corona_del_col을 대신하겠다 '종랑구':'중랑구', '한국':'기타' 이렇게 


# In[29]:


# 이상치가 처리된 데이터를 다시 출력해 봅시다.
plt.figure(figsize=(20,10))
sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False},
        style='darkgrid')
ax = sns.countplot(x="지역", data=corona_out_region, palette="Set2")


#  

# ### 3.5. 8월달 지역별 확진자 수 출력

# 감염자가 많았던 8월에는 지역별로 확진자가 어떻게 분포되어 있는지 막대그래프로 출력해 봅시다.  (앞에서는 날짜별 지역별로 확진사 수를 분석했는데 두개조건을 모두 반영해보겠음)

# In[30]:


# 논리연산을 이용한 조건을 다음과 같이 사용하면 해당 조건에 맞는 데이터를 출력할 수 있습니다.
corona_out_region[corona_del_col['month'] == '8']


# In[31]:


# 그래프를 출력합니다.   3.4에서 사용한 코드와 거의비슷 
plt.figure(figsize=(20,10))
sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False},
        style='darkgrid')
ax = sns.countplot(x="지역", data=corona_out_region[corona_del_col['month'] == '8'], palette="Set2")
# 8월 데이터만 사용        8월에는 성북구가 가장 많았음 
#위에서 전체적으로 봤을때는 관악구가 가장 많았지만


#  

# ### 3.6. 월별 관악구 확진자 수 출력

# 이번에는 확진자가 가장 많았던 관악구 내의 확진자 수가 월별로 어떻게 증가했는지 그 분포를 막대그래프로 출력해 봅시다.   (이때는 month와 지역구 두개의 조건을 같이 붙임)

# In[32]:


# 해당 column을 지정하여 series 형태로 출력할 수 있습니다.
corona_out_region['month'][corona_out_region['지역'] == '관악구']


# In[33]:


# 그래프를 출력합니다.  앞에 3.2. 코드와 거의비슷함

plt.figure(figsize=(10,5))
sns.set(style="darkgrid")
ax = sns.countplot(x="month", data=corona_out_region[corona_out_region['지역'] == '관악구'], palette="Set2", order = order)
# 지역 관악구만 불러 오겠음  


#  

# ### 3.7. 서울 지역에서 확진자를 지도에 출력

# 지도를 출력하기 위한 라이브러리로 folium을 사용해 봅시다.

# In[34]:


# 지도 출력을 위한 라이브러리 folium을 import 합니다.
import folium  # 오픈 스트릿 웹과 같은 지도데이터에 위치 정보를 시각화 하는 라이브러리임 
# 우리가 일반적으로 지도를 펼쳐서 위치를 확인할때 위도, 경도 사용하는데 여기서도 마찮가지임

# Map 함수를 사용하여 지도를 출력합니다.
map_osm = folium.Map(location=[37.529622, 126.984307], zoom_start=11)
# osm 오픈 스트릿 맵 약자    위도, 경도 (서울시 어느지역에) zoom_start초기 화면 크기 지정
map_osm


#  

# 지역마다 지도에 정보를 출력하기 위해서는 각 지역의 좌표정보가 필요합니다.
# 
# 이를 해결하기 위해서 서울시 행정구역 시군 정보 데이터를 불러와 사용합니다.
# 
# 데이터 출처: https://data.seoul.go.kr/dataList/OA-11677/S/1/datasetView.do

# In[35]:


# CRS에 저장합니다.
CRS=pd.read_csv("./data/서울시 행정구역 시군구 정보 (좌표계_ WGS1984).csv")


# In[36]:


# Dataframe을 출력해 봅니다.   # 시군구 별로 위도 경도 데이터가 나옴 
CRS


#  

# 저장된 데이터에서 지역명이 서울의 중심지 `중구`인 데이터를 뽑아봅시다.

# In[37]:


CRS[CRS['시군구명_한글'] == '중구']


#  

# 이제 for 문을 사용하여 지역마다 확진자를 원형 마커를 사용하여 지도에 출력해 봅시다.

# In[38]:


# corona_out_region의 지역에는 'oo구' 이외로 `타시도`, `기타`에 해당되는 데이터가 존재 합니다.
# 위 데이터에 해당되는 위도, 경도를 찾을 수 없기에 삭제하여 corona_seoul로 저장합니다.
corona_seoul = corona_out_region.drop(corona_out_region[corona_out_region['지역'] == '타시도'].index)
corona_seoul = corona_seoul.drop(corona_out_region[corona_out_region['지역'] == '기타'].index)
# 이렇게 새변수에 지워서 저장을 해주었음 

# 서울 중심지 중구를 가운데 좌표로 잡아 지도를 출력합니다.
map_osm = folium.Map(location=[37.557945, 126.99419], zoom_start=11)

# 지역 정보를 set 함수를 사용하여 25개 고유의 지역을 뽑아냅니다.
for region in set(corona_seoul['지역']):

    # 해당 지역의 데이터 개수를 count에 저장합니다.
    count = len(corona_seoul[corona_seoul['지역'] == region])
    # 해당 지역의 데이터를 CRS에서 뽑아냅니다.
    CRS_region = CRS[CRS['시군구명_한글'] == region]

    # CircleMarker를 사용하여 지역마다 원형마커를 생성합니다.
    marker = folium.CircleMarker([CRS_region['위도'], CRS_region['경도']], # 위치
                                  radius=count/10 + 10,                 # 범위 (원 크기)
                                  color='#3186cc',            # 선 색상
                                  fill_color='#3186cc',       # 면 색상
                                  popup=' '.join((region, str(count), '명'))) # 팝업 설정 (각지역구 몇명의 확진자가 있는지 숫자 보기 좋게 하기위해서)
                                # 이때 팝업으로 뜨는 정보는 3가지에 정보를 조인 한것인데요  명 단위까지 넣음

    # 생성한 원형마커를 지도에 추가합니다.  add_to 함수사용
    marker.add_to(map_osm)

map_osm


# #### 퀴즈 2. 6월에 확진자가 가장 많이 나온 지역을 구하세요.

# In[39]:


top = corona_out_region[corona_del_col['month'] == '6']['지역'].value_counts()
top.index[0] # 내림차순 정렬되서 인덱스 0번 부르면 가장 많이 나온 지역임 


# In[40]:


# 6월에 확진자가 가장 많이 나온 지역을 구하여 quiz_2 변수에 저장합니다.
# 문자형으로 저장합니다.
quiz_2 = top.index[0]


#  ---

# ## 제출하기

# 퀴즈 1번과 2번을 수행 후, 아래 코드를 실행하면 `quiz_1 ~ 2` 변수가 저장된 csv 파일을 제작하여 채점을 받을 수 있습니다.
# 
# **아래 코드를 수정하면 채점이 불가능 합니다.**

# In[41]:


answer=pd.read_csv('submission.csv')
answer.loc[0]['quiz_2']


# In[42]:


d = {'quiz_1': [quiz_1], 'quiz_2': [quiz_2]}
df_quiz = pd.DataFrame(data=d)
df_quiz.to_csv("submission.csv",index=False)


# In[43]:


# 채점을 수행하기 위하여 로그인
import sys
sys.path.append('vendor')
from elice_challenge import check_score, upload


# In[44]:


# 제출 파일 업로드
await upload()


# In[45]:


# 채점 수행
await check_score()


# ---

# <span style="color:rgb(120, 120, 120)">본 학습 자료를 포함한 사이트 내 모든 자료의 저작권은 엘리스에 있으며 외부로의 무단 복제, 배포 및 전송을 불허합니다.
# 
# Copyright @ elice all rights reserved</span>
