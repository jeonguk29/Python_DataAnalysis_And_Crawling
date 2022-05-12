#!/usr/bin/env python
# coding: utf-8

# # [Project 3] 자동차 리콜 데이터 분석

# ---

# ## 프로젝트 목표
# - 한국교통안전공단 자동차 결함 리콜 데이터를 분석하여 유의미한 정보 도출
# - 탐색적 데이터 분석을 수행하기 위한 데이터 정제, 특성 엔지니어링, 시각화 방법 학습

# ---

# ## 프로젝트 목차
# 1. **데이터 읽기:** 자동차 리콜 데이터를 불러오고 Dataframe 구조를 확인<br>
#     1.1. 데이터 불러오기<br>
# <br> 
# 2. **데이터 정제:** 결측치 확인 및 기초적인 데이터 변형<br>
#     2.1. 결측치 확인<br>
#     2.2. 중복값 확인<br>
#     2.3. 기초적인 데이터 변형<br>
# <br>
# 3. **데이터 시각화:** 각 변수 별로 추가적인 정제 또는 feature engineering 과정을 거치고 시각화를 통하여 데이터의 특성 파악<br>
#     3.1. 제조사별 리콜 현황 출력<br>
#     3.2. 모델별 리콜 현황 출력<br>
#     3.3. 월별 리콜 현황 출력<br>
#     3.4. 생산연도별 리콜 현황 출력<br>
#     3.5. 4분기 제조사별 리콜 현황 출력<br>
#     3.6. 하반기 생산연도별 리콜 현황 출력<br>
#     3.7. 워드 클라우드를 이용한 리콜 사유 시각화<br>

# ---

# ## 데이터 출처
# -  https://www.data.go.kr/data/3048950/fileData.do

# ---

# ## 프로젝트 개요
# 
# 리콜(recall)은 제품의 설계, 제조 단계에서 결함이 발견되었을 시 문제 예방의 차원에서 판매자가 무상으로 수리, 점검 및 교환을 해주는 소비자 보호 제도입니다. 집집마다 개인용 자동차를 보유하게 되면서 자동차는 어느덧 우리 삶의 일상재가 되었지만, 안전성에 대해서는 산발적인 문제 제기가 계속되고 있고, 이에 따라 전격적인 자동차 리콜 사태도 종종 발생하여 화제를 모으곤 합니다.
# 
# 이번 프로젝트에서는 한국교통안전공단에서 제공한 2020년 자동차 결함 리콜 데이터를 활용하여 유의미한 패턴 및 인사이트를 발굴하고 시각화하는 실습을 진행하도록 하겠습니다.

# ---

# ## 1. 데이터 읽기

# 필요한 패키지 설치 및 `import`한 후 `pandas`를 사용하여 데이터를 읽고 어떠한 데이터가 저장되어 있는지 확인합니다.

# ### 1.1. 데이터 불러오기

# In[9]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt # 여기까지가 데이터 분석에 있어서 가장 기본적인 라이브러리 
get_ipython().system('pip install seaborn==0.9.0 # seaborn  라이브러리 버전 통일을 위해서 사용 ')
import seaborn as sns    # 조금더 깔끔한 시각화를 위해 설치하는 코드 
print(sns.__version__)
# missingno라는 라이브러리가 설치되어 있을 경우 import
try: 
    import missingno as msno   # 결측치 시각화 위한 라이브러리 
# missingno라는 라이브러리가 설치되어 있지 않을 경우 설치 후 import 
except: 
    get_ipython().system('pip install missingno')
    import missingno as msno


# In[10]:


# pd.read_csv를 통하여 dataframe 형태로 읽어옵니다.
df = pd.read_csv("./data/한국교통안전공단_자동차결함 리콜현황_20201231.csv", encoding="euc-kr")
# "euc-kr" 우리말 인코딩할때 사용 


# In[11]:


# 상위 5개 데이터를 출력합니다.
df.head()


# In[12]:


# 상위 10개 데이터를 출력합니다.
df.head(10)


# In[13]:


# 하위 5개 데이터를 출력합니다.  # 보면 0부터 1274 즉 1275개의 low가 있군아 알수 있음 
df.tail()


# In[14]:


# dataframe 정보를 요약하여 출력합니다. 
df.info()   #null 값이 없는 걸 확인 할수 있음 


# ---

# ## 2. 데이터 정제

# 데이터를 읽고 확인했다면 결측값(missing data), 중복값(duplicates)을 처리하고 열 이름 변경과 같은 기초적인 데이터 변형을 진행해봅시다.

# ### 2.1. 결측치 확인

# `missingno.matrix()` 함수를 이용하여 결측치를 시각화해봅시다.

# In[15]:


import matplotlib.font_manager as fm

# 시각화를 이용해 결측치 확인 
"""
지금 데이터가 다 한국말로 되어 있음 대부분 라이브러리들이 우리말로 시각화 하려고하면 대부분 깨짐 
그래서 한국어를 제대로 시각화 하기위해서 폰트등록을 해서 지정을 해줘야하는 약간의 번거로움이 있음  그래서 font_manager를 불러옴 
"""
font_dirs = ['/usr/share/fonts/truetype/nanum', ]  # 폰트 설치되어있는 디렉토리 
font_files = fm.findSystemFonts(fontpaths=font_dirs) # 폰트 저장경로에서 폰트파일 찾아서 다 저장해라 

for font_file in font_files:  # 여러개에 폰트들이 폴더에 설치되어 있을지도 모르니 반복문을 이용해 각각 다 추가시켜줌 
    fm.fontManager.addfont(font_file)


# In[16]:


sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False})  # 등록했던 폰트 설정 마이너스 기호 깨짐 방지 "axes.unicode_minus":False
msno.matrix(df) # 이렇게 df 통째로 보내면 df열별로 결측값이 얼마나 있는지 시각화 가능함 
plt.show() # 다 검정으로 나오는데 그러면 각 컬럼들에 있어서 결측치가 없다는 것임 


# `isna()` 함수를 이용하여 결측치를 확인해봅시다.

# In[17]:


# 각 열 별로 결측치의 갯수를 반환합니다. (True:1, False:0)
df.isna().sum()          # 시각화가 아닌 계산을 통한 결측치 반환 어떤 값이 na(낫 어베일어블) 결측치냐 아니냐  그걸 다 sum 해라 


# ### 2.2. 중복값 확인

# `duplicated()` 함수를 이용하여 중복값을 확인해봅시다.

# In[18]:


df[df.duplicated(keep=False)]   # 데이터 분석전에 중복값 확인해주는게 좋음  중복값 꺼내주는 판다스 함수 duplicated
# 34 82 가 모든 컬럼이 일치함 


# `drop_duplicates()` 함수를 이용하여 중복값을 제거합니다.

# In[20]:


print("Before:", len(df))
df = df.drop_duplicates() # 중복값 제거 함수 drop_duplicates()
print("After:", len(df))  # 이렇게 결측치 확인 중복값 확인은 데이터 분석에 있어서 거의 항상 진행하는 단계임 


# ### 2.3. 기초적인 데이터 변형

# 현재 `생산기간`, `생산기간.1`, `리콜개시일` 열은 모두 `object` 타입, 즉 문자열로 인식되고 있습니다. 분석을 위해 연도, 월, 일을 각각 정수형으로 저장합니다. <br>
# 추가적으로 분석의 편리를 위해 열 이름을 영어로 바꿔줍니다.       + object는 string을 의미함 

# In[21]:


def parse_year(s):  # 문자열에서 년도, 월, 일 만 추출하는 함수들  
    return int(s[:4]) # 0 1 2 3 가져와서 int형으로 바꿔라   ex 2014-05-28 이런식이니까  
def parse_month(s):
    return int(s[5:7])
def parse_day(s):
    return int(s[8:])

# Pandas DataFrame에서는 row별로 loop를 도는 것이 굉장히 느리기 때문에, apply() 함수를 이용하여 벡터 연산을 진행합니다.
df['start_year'] = df['생산기간'].apply(parse_year)
df['start_month'] = df['생산기간'].apply(parse_month)
df['start_day'] = df['생산기간'].apply(parse_day)

df['end_year'] = df['생산기간.1'].apply(parse_year)
df['end_month'] = df['생산기간.1'].apply(parse_month)
df['end_day'] = df['생산기간.1'].apply(parse_day)

df['recall_year'] = df['리콜개시일'].apply(parse_year)
df['recall_month'] = df['리콜개시일'].apply(parse_month)
df['recall_day'] = df['리콜개시일'].apply(parse_day)

df.head(3) # 표보면 각각 분리된걸 확인할수 있음 


# In[22]:


# 불필요한 열은 버리고, 열 이름을 재정의합니다.
df = df.drop(columns=['생산기간', '생산기간.1', '리콜개시일']).rename(columns={'제작자': "manufacturer", "차명": "model", "리콜사유": "cause"})
df.head(3)    # 영어로 다 바꾸주겠음


# 본 분석에서는 2020년의 데이터만을 대상으로하므로, 그 외의 데이터가 있다면 삭제해주겠습니다.

# In[23]:


# 2019년의 데이터가 함께 존재함을 알 수 있습니다.
df.recall_year.min(), df.recall_year.max()        # 2019년도 값도 데이터 셀에 있다는 걸 확인할 수 있음 


# In[24]:


# 2020년의 데이터만을 남겨줍니다.
df = df[df['recall_year']==2020]   # 2020놈들만 남겨서 다시 저장 
len(df) 


# ---

# ## 3. 데이터 시각화

# 각 column의 변수별로 어떠한 데이터 분포를 하고 있는지 시각화를 통하여 알아봅시다.

# ### 3.1. 제조사별 리콜 현황 출력

# 제조사별 리콜 건수 분포를 막대 그래프로 확인해보겠습니다.

# In[25]:


df.head()


# In[26]:


df.groupby("manufacturer").count()["model"].sort_values(ascending=False)  # 같은 제조사 끼리 그룹바이 해줌  값이큰 순서별로 내림차순 


# In[28]:


pd.DataFrame(df.groupby("manufacturer").count()["model"].sort_values(ascending=False)).rename(columns={"model": "count"})
# 모델이름을 카운트로 바꿔서 가져오겠음  모기좋게 하기위해 DataFrame 함수 사용 
#아래 표를 보면 manufactuer은 아래에 있는데 이 데이터 프레임에서 인덱스로 취급되고 있다는 뜻임 


# In[30]:


tmp = pd.DataFrame(df.groupby("manufacturer").count()["model"].sort_values(ascending=False)).rename(columns={"model": "count"})
# 일단 위에코드를 임시 변서 tmp에 저장해주겠음 
tmp


# In[33]:


plt.figure(figsize=(20,10))    # 카운트 시각화 해볼 것임 
# 한글 출력을 위해서 폰트 옵션을 설정합니다.
sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False},
        style='darkgrid')
ax = sns.countplot(x="manufacturer", data=df, palette="Set2", order=tmp.index)
# .countplot 이용해 manufacturer에 카운트를 시각화 할것임 tmp 따로 저장한 이유는  order 지정해주기 위함임 
plt.xticks(rotation=270) # 가로축에 이름들이 곂쳐보여서 270회전으로 제조 회사이름 출력함 
plt.show()


# In[35]:


tmp.index


# ### 3.2. 모델별 리콜 현황 출력

# 차량 모델별 리콜 건수 분포를 막대 그래프로 확인해보겠습니다.

# In[36]:


pd.DataFrame(df.groupby("model").count()["start_year"].sort_values(ascending=False)).rename(columns={"start_year": "count"}).head(10)


# 모델은 굉장히 많으므로, 상위 50개 모델만 뽑아서 시각화를 진행해보겠습니다.

# In[38]:


tmp = pd.DataFrame(df.groupby("model").count()["manufacturer"].sort_values(ascending=False))
tmp = tmp.rename(columns={"manufacturer": "count"}).iloc[:50] # iloc[:50] 인덱스로 슬라이싱 하는 함수 


# In[39]:


# 그래프의 사이즈를 조절합니다.
plt.figure(figsize=(10,5))

# seaborn의 countplot 함수를 사용하여 출력합니다.
sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False},
        style='darkgrid')
ax = sns.countplot(x="model", data=df[df.model.isin(tmp.index)], palette="Set2", order=tmp.index)# model 컬럼안에 
# isin(tmp.index)  tmp  인덱스 안에 즉 모델명이 상위 50개인 값만 가져와라 
plt.xticks(rotation=270)
plt.show()


# ### 3.3. 월별 리콜 현황 출력

# 월별 리콜 건수 분포를 막대 그래프로 확인해보겠습니다.

# In[40]:


pd.DataFrame(df.groupby("recall_month").count()["start_year"].sort_values(ascending=False)).rename(columns={"start_year": "count"})


# In[41]:


# 그래프의 사이즈를 조절합니다.
plt.figure(figsize=(10,5))

# seaborn의 countplot 함수를 사용하여 출력합니다.
sns.set(style="darkgrid")
ax = sns.countplot(x="recall_month", data=df, palette="Set2") # 월별로 보는게 편해서 딱히 oder주지 않겠음 
plt.show()


# ### 3.4. 생산연도별 리콜 현황 출력

# 이번에는 생산연도별 리콜 현황을 꺾은선 그래프로 알아보겠습니다.

# In[45]:


tmp = pd.DataFrame(df.groupby("start_year").count()["model"]).rename(columns={"model": "count"}).reset_index()
tmp.head() # reset_index() 해줘서 그룹바이 했던 "start_year"변수가 인덱스로 들어있지 않고 새로운 변수가 인덱스로 들어왔음 


# In[47]:


tmp = pd.DataFrame(df.groupby("start_year").count()["model"]).rename(columns={"model": "count"}).reset_index()

# 그래프의 사이즈를 조절합니다.
plt.figure(figsize=(10,5))

# seaborn의 countplot 함수를 사용하여 출력합니다.
sns.set(style="darkgrid")
sns.lineplot(data=tmp, x="start_year", y="count") # 한글이용이 아니라 그냥 년도 숫자로 표시할거라 폰트 지정 따로 안해주겠음  lineplot 이용하면 꺽은선 그레프 사용가능 
plt.show()


# In[48]:


tmp


# #### 퀴즈 1. 2020년에 리콜 개시가 가장 많이 일어난 달(month)과 가장 적게 일어난 달의 차이(건수)를 구하세요.

# In[49]:


tmp = pd.DataFrame(df.groupby("recall_month").count()["start_year"].sort_values(ascending=False)).rename(columns={"start_year": "count"})
# 내림차순 정렬이라 0번째가 가장 크고 가장 아래가 가장 작은 값일것임 
tmp.iloc[0]["count"]-tmp.iloc[-1]["count"] # 0번째 값 카운트 가져오고 -1 가장 마지막 값 이랑 빼주면 됨


# In[50]:


# 퀴즈의 답을 구하여 quiz_1 변수에 저장합니다.
# integer 형 상수값으로 저장합니다.
quiz_1 = 194


# ### 3.5. 4분기 제조사별 리콜 현황 출력

# 가장 최근 데이터인 2020년 4분기(10, 11, 12월) 제조사별 리콜 현황을 시각화해봅시다.

# In[51]:


# 논리연산을 이용한 조건을 다음과 같이 사용하면 해당 조건에 맞는 데이터를 출력할 수 있습니다.
df[df.recall_month.isin([10,11,12])].head() 


# In[52]:


# 그래프를 출력합니다.
plt.figure(figsize=(20,10))
sns.set(font="NanumBarunGothic", 
        rc={"axes.unicode_minus":False},
        style='darkgrid')
ax = sns.countplot(x="manufacturer", data=df[df.recall_month.isin([10,11,12])], palette="Set2") #x축 제조사 별로 데이터는 4분기 월 이용
plt.xticks(rotation=270)
plt.show()


# ### 3.6. 하반기 생산연도별 리콜 현황 출력

# 이번에는 2020년 하반기(7~12월)에 개시된 리콜 건들을 생산 개시 연도를 기준으로 시각화해봅시다.

# In[53]:


# 해당 column을 지정하여 series 형태로 출력할 수 있습니다.
df[df.recall_month>=7].head() # month를 정수형태로 저장해줬기 때문에 이런식으로도 가능함 


# In[55]:


# 그래프를 출력합니다.
plt.figure(figsize=(10,5))
sns.set(style="darkgrid")
ax = sns.countplot(x="start_year", data=df[df.recall_month>=7], palette="Set2") # 한글 따로 주지 않음  년도별로 하반기 진행 건만 나와있음 
plt.show()


# ### 3.7. 워드 클라우드를 이용한 리콜 사유 시각화

# 워드 클라우드를 이용하여 리콜 사유를 시각화해보도록 하겠습니다.

# In[59]:


df.cause # 이런데이터를 값이 딱딱 떨어지는 데이터가 아니라 비정형 데이터라고 함 
#이렇게 글로 처리되어있을때 많이 사용하는 방법중 하나가 워드 클라우드임 


# In[62]:


# 워드 클라우드 생성을 도와주는 패키지를 가져옵니다.
try:
    from wordcloud import WordCloud, STOPWORDS
except:
    get_ipython().system('pip install wordcloud')
    from wordcloud import WordCloud, STOPWORDS # STOPWORDS 이것은 무엇이냐 WordCloud만들때 유의미한 시각화가 되기 위해서 
    # 문법적인 성분에 해당하는 언어들을 배제 해주기위한 집합임 


# In[61]:


# 문법적인 성분들을 배제하기 위해 stopwords들을 따로 저장해둡니다.
set(STOPWORDS)


# 영어를 사용할 때는 상관 없지만, 우리말을 쓸 때에는 적합하지 않습니다. 여기서는 예시로 몇 개의 stopwords들을 수기로 저장해보겠습니다.

# In[67]:


# 손으로 직접 리콜 사유와 관련이 적은 문법적 어구들을 배제해보겠습니다.
spwords = set(["동안", "인하여", "있는", "경우", "있습니다", "가능성이", "않을", "차량의", "가", "에", "될", "이",
               "인해", "수", "중", "시", "또는", "있음", "의", "및", "있으며", "발생할", "이로", "오류로", "해당"])
#spwords =set()    


# In[64]:


df.cause


# In[65]:


# 리콜 사유에 해당하는 열의 값들을 중복 제거한 뒤 모두 이어붙여서 text라는 문자열로 저장합니다.
text = ""

for c in df.cause.drop_duplicates():
    text += c

text[:100]


# 워드 클라우드를 생성하고 시각화해보겠습니다.

# In[69]:


# 한글을 사용하기 위해서는 폰트를 지정해주어야 합니다.
wc1 = WordCloud(max_font_size=200, stopwords=spwords, font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
                background_color='white', width=800, height=800)
wc1.generate(text)

plt.figure(figsize=(10, 8))
plt.imshow(wc1)
plt.tight_layout(pad=0)
plt.axis('off')
plt.show()


# #### 퀴즈 2. 기아자동차(주)의 제품 중 가장 최근에 리콜이 개시된 제품의 모델명을 구하세요. 

# In[70]:


df[df['manufacturer']=="기아자동차(주)"].sort_values(by=["recall_year", "recall_month", "recall_day"], ascending=False).iloc[0]['model']
   # 년도로 일단 정렬 년도 같으면 월로 정렬 그다음 일로 정렬 


# In[73]:


# 퀴즈의 답을 구하여 quiz_2 변수에 저장합니다.
# 문자형으로 저장합니다.
quiz_2 =  df[df['manufacturer']=="기아자동차(주)"].sort_values(by=["recall_year", "recall_month", "recall_day"], ascending=False).iloc[0]['model']


#  ---

# ## 제출하기

# 퀴즈 1번과 2번을 수행 후, 아래 코드를 실행하면 `quiz_1 ~ 2` 변수가 저장된 csv 파일을 제작하여 채점을 받을 수 있습니다.
# 
# **아래 코드를 수정하면 채점이 불가능 합니다.**

# In[74]:


d = {'quiz_1': [quiz_1], 'quiz_2': [quiz_2]}
df_quiz = pd.DataFrame(data=d)
df_quiz.to_csv("submission.csv",index=False)


# In[75]:


answer=pd.read_csv('submission.csv')
answer.loc[0]['quiz_2']


# In[76]:


# 채점을 수행하기 위하여 로그인
import sys
sys.path.append('vendor')
from elice_challenge import check_score, upload


# In[77]:


# 제출 파일 업로드
await upload()


# In[78]:


# 채점 수행
await check_score()

