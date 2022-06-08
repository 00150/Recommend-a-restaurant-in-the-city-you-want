#0. 사용할 패키지 가져오기
from multiprocessing import connection
import pandas as pd
from soupsieve import select
import numpy as np
import os
import sqlite3
import psycopg2
import csv
import logging

#Part 1. 데이터 전처리 

#1. 사용할 데이터의 경로 설정 및 데이터 가져오기.
data = os.path.join(os.getcwd(),'경기상권정보.csv')
df = pd.read_csv(data)


#2. 음식에 해당하는 데이터만 출력 및 사용할 컬럼만 지정하기.
df = df.loc[df['상권업종대분류명'] == '음식']

columns =['상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도']
df = df[columns]


#3. 입력하는 동을 기준으로, 원하는 데이터만 출력 및 따로 저장하기. 
#3-1. 찾고자 하는 동의 이름을 입력 받습니다.

dong = input('찾고자하는 동네의 동 이름을 입력하세요😆 : ').replace(" ", '').split(',') # 은행2동, 장항2동, 와동
select_dong = dong

# # ---> 함수를 생성하여 이용하겠습니다.
def mapping_address():
      #3-1. 찾고자 하는 동의 이름을 입력 받습니다.
  #dong = input('찾고자하는 동네의 동 이름을 입력하세요😆 : ').replace(" ", '').split(',') # 은행2동, 장항2동, 와동
  dong_name = select_dong

  #3-2. 기본 데이터 생성
  default_data = pd.DataFrame(columns = {'상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도'})  

  #3-3. for문을 통해 기입한 동이름으로만 데이터를 따로 구성합니다.
  for number in range(len(dong_name)):
    add_df = df.loc[(df['행정동명'] == dong_name[number])]
    default_data = pd.concat([add_df, default_data])
  
  #3-4.컬럼명 단순화
  # 추려진 데이터를 확인해보면 컬럼명의 어휘가 조금 어렵습니다. 보다 이용에 편리하도록 편리한 컬럼명으로 바꿔줍니다.
  default_data.columns = ['상호명',
                          '업종중분류명',
                          '업종소분류명',
                          '표준산업분류명',
                          '행정동명',
                          '위도',
                          '경도']

  
  #3-5. 원하는 지역으로 구성된 데이터프레임을 따로 저장합니다.
  default_data.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/SELECT_REGION.csv', index = False, encoding= 'cp949')
  


#4. 이후 생성된 데이터를 클라우드 데이터 서비스에 저장하도록 합니다.
#   Postgre 데이터베이스 서버와 연결 -> 클라우드 데이터베이스에서 생성한 elephantDB를 대상으로 합니다.
#   데이터베이스에 연결할 때, 필요한 정보들을 사전에 변수에 담아 놓습니다.

host = 'castor.db.elephantsql.com'
user = 'iejeegfa'
password = 'qjLvYChc-r75m8BZoQFRgNzRWlhNfV4U'
database = 'iejeegfa'

#4-1. 연결 & 테이블 생성 & 테이블 삽입을 진행할 함수를 작성합니다.

def connect_sql():
  
  # 연결 및 에러 제어 
  try:
    connection = psycopg2.connect(
      host = host,
      user = user,
      database = database,
      password = password)
    cur = connection.cursor()
  
  except:
    logging.error("could not connect to rds")
  
  
  # 테이블 생성.
  cur.execute("DROP TABLE IF EXISTS SELECT_REGION;")
  cur.execute("""CREATE TABLE SELECT_REGION(
    Id INTEGER,
    상호명 VARCHAR(128),
    업종중분류명 VARCHAR(128),
    업종소분류명 VARCHAR(128),
    표준산업분류명 VARCHAR(128),
    행정동명 VARCHAR(128),
    위도 FLOAT8,
    경도 FLOAT8
  );""")
  
  
  # 데이터 삽입.  
  with open('SELECT_REGION.csv', 'r') as f:
    try:
      reader = csv.reader(f)
      next(reader)
      for id, row in enumerate(reader, start=1):
        cur.execute("""INSERT INTO SELECT_REGION(Id, 상호명, 업종중분류명,
                              업종소분류명, 표준산업분류명, 행정동명, 위도, 경도) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                              (id, row[0],row[1], row[2], row[3], row[4], row[5], row[6]))
      print('mission complete❗')      
    
    except:
      logging.error("can't insert data")
      
  connection.commit()
  connection.close() 
  

#🔆  지금까지 만든 함수는 다음과 같습니다.
#(1). 원하는 지역만 맵핑하여 데이터 추출(생성)
#(2). 이후 클라우드데이터 서비스 연결(Postgress) 
#     생성된 함수를 이용하여 함수를 출력하여 봅시다.

#(1). 데이터 추출 
mapping_address()

#(2). DB 연결 및 데이터 삽입
connect_sql()

#------------------------------------------🔰🔰🔰🔰🔰 PART. 2 🔰🔰🔰🔰🔰------------------------------------------------
# 요식업 전체의 카테고리 데이터 활용하기. ---> '코사인 유사도' 이용하기.
# 우리가 원하는 지역만을 맵핑하여 만든 데이터의 컬럼들중, '중분류명'과 '소분류명'은 활용가치가 큰 데이터입니다.
# 이 데이터들을 Cartegory 데이터라고 지칭하겠습니다.

# 이 데이터들을 하나의 컬럼으로 몰아두고, 이를 바탕으로 코사인 유사도를 적용하도록 하겠습니다.
# https://innate-clove-c5b.notion.site/Cosine-Similarity-664f643b74a54a338065b7a3869576ab(내 노션 -> 코사인 유사도 정리)
#❗ 간단하게 설명하자면, 텍스트를 기반으로 가장 쉽게 '비슷함의 정도'를 파악하여 줍니다.


#1. 데이터 불러오기.
scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\SELECT_REGION.csv'
select_df = pd.read_csv(scv_url, encoding= 'cp949')


#❗ 위에서 언급한 카테고리 데이터들의 모습은 다음과 같습니다.
#->양식            정통양식/경양식  
#->커피점/카페     커피전문점/카페/다방
#->한식           한식/백반/한정식


#❗이런 키워드를 담은 데이터들을 하나의 컬럼에 몰아두면 유사도를 계산할 수 있습니다.
#->양식            정통양식/경양식          ------------> 양식 전통양식 경양식
#->커피점/카페     커피전문점/카페/다방      ------------> 커피점 카페 커피전문점 카페 다방
#->한식           한식/백반/한정식           ------------> 한식 한식 백반 한정식


#2. 카테고리 데이터들을 하나로 묶어주는 전처리를 진행합니다.
select_df['합친데이터'] = select_df['업종중분류명'] + select_df['업종소분류명'] +select_df['표준산업분류명'] 


#3. 하나로 뭉쳐진 카테고리 텍스트 데이터를 '피처 벡터화'하고 코사인 유사도를 계산하는 코드를 작성합니다.(사이킷런)
import sklearn
from sklearn.feature_extraction.text import CountVectorizer  # 피체 벡터화
from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도

#🔆CountVectorizer 
# 1. 문서를 토큰 리스트로 변환한다.
# 2. 각 문서에서 토큰의 출현 빈도를 센다.
# 3. 각 문서를 BOW 인코딩 벡터로 변환한다.

count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2)) 
# min_df : 단어장에 포함되기 위한 최소 빈도 (※ 기본값 : 1)
# ngram_range:  n-그램 범위로 단어를 몇 개로 토큰화 할지를 의미합니다.


place_category = count_vect_category.fit_transform(select_df['합친데이터'])
applied_cosine = cosine_similarity(place_category, place_category)
place_simi_cate_sorted_ind = applied_cosine.argsort()[:, ::-1]
#이렇게 하면, 각각의 데이터 vs 데이터들이 서로 카테고리 텍스트가 얼마나 유사한지를 따져줍니다.
#500개의 데이터가 있다면 1번은 자기 자신과 한 번 비교하고, 나머지 499개와 비교를 하게 됩니다.
#이 데이터를 바탕으로 마지막 단계에서 최종 채점 단계에서 활용합니다.



# 직접 작성한 패키지명과 모듈 이름입니다. 
# 이 안에 작성된 함수를 사용하기 위해 불러옵니다.
from selfmade_function import Handmade_selenium as fc


# 만든 함수는 다음과 같습니다.
"""
📜 part1. 가게의 url을 컬럼으로 저장하는 함수를 생성
add_url_column(df) / return None / csv 파일 반환 (add_url.csv)


📜 part2. 가게의 주소를 크롤링하는 함수
add_address(df) / return None / csv 파일 반환 (add_url_address.csv)


📜 part3. 가게의 평점을 크롤링하는 함수
add_store_score(df) / return None / csv 파일 반환 (add_url_address_score.csv)


📜 part4. 가게의 리뷰를 크롤링하는 함수
add_review_text(df)  / return None / csv 파일 반환
"""




# url을 컬럼으로 저장하는 함수를 사용하기 위해, 포털에 검색할 키워드를 정리합니다.
select_df['네이버키워드'] = select_df['행정동명'] + "%20" + select_df['상호명']  #❗ "%20"은 띄어쓰기를 의미합니다.
select_df['naver_store_url'] = ''

# 이후, 함수를 사용합니다.
# 가게의 url을 컬럼으로 생성합니다.

#📜 part1. 가게의 url을 컬럼으로 저장하는 함수를 생성
fc.add_url_column(select_df)

#📜 part2. 가게의 주소를 크롤링하는 함수
scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\add_url.csv'
df1 = pd.read_csv(scv_url, encoding= 'cp949')
fc.add_address(df1)


#📜 part3. 가게의 평점을 크롤링하는 함수
scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\add_url_address.csv'
df2 = pd.read_csv(scv_url, encoding= 'cp949')
fc.add_store_score(df2)


#📜 part4. 가게의 리뷰를 크롤링하는 함수
scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\(add_url_address_score.csv'
df3 = pd.read_csv(scv_url, encoding= 'cp949')
fc.add_review_text(df3)



#-------❗❗❗❗❗밑 부분은 제대로 작동되는 코드이지만, 작성한 패키지의 함수를 사용하기 위해 주석처리합니다.❗❗❗❗❗--------



# #4. 포털의 블로그 리뷰등을 이용하여 별점 데이터를 가져와 데이터로 활용한다.
# #   공공데이터로 확보한 상호명, 행정동 명을 검색어로 변환하여 포털에 검색하기.
# #   셀레늄 크롤러를 통해 검색 결과로 나온 블로그 리뷰, 블로그 별점 데이터 확보하기.

# #🔆 사용할 라이브러리를 불러옵니다.
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# import time

# # 셀레니움을 사용하기 위해 다운로드한 크롬 드라이버의 경로를 작성합니다. 
# # ※ 현재 작업중에 있는 코드파일의 디렉토리에 함께 위치하는 것이 베스트인 것 같슴다..
# chromedriver = r'C:\Users\j.park\Section3\real_project3\chromedriver.exe'
# driver = webdriver.Chrome(chromedriver)


# # 크롤링으로 데이터를 얻어올 곳은 네이버로 진행하겠습니다.
# # 네이버 지도 검색창에 [~동 ~~식당]으로 검색하여 정확도를 높혀줍니다. 검색어를 미리 설정하여줍시다.
# select_df['네이버키워드'] = select_df['행정동명'] + "%20" +select_df['상호명'] #❗ "%20"은 띄어쓰기를 의미합니다.
# select_df['naver_store_url'] = ''




#-------❗❗❗❗❗밑 부분은 제대로 작동되는 코드이지만, 작성한 패키지의 함수를 사용하기 위해 주석처리합니다.❗❗❗❗❗




# # 본격적으로 가게 상세페이지의 URL을 가져오도록 합니다.

# for i, keyword in enumerate(select_df['네이버키워드'].tolist()):  #tolist를 이용, 객체 생성
#   print("이번에 찾을 키워드는 다음과 같습니다 :", i, f'/{select_df.shape[0]-1}행', keyword) #csv 파일의 첫번째 행에 컬럼이 담겨있으므로 제외.
    
#   try:
#       naver_map_search_url = f'https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5'  # 현재 주소는 모바일입니다.
#       driver.get(naver_map_search_url)    
#       time.sleep(3.5)    
#       select_df.iloc[i,-1] = driver.find_element_by_css_selector(
#           '#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview').get_attribute('data-cid')
#       # 네이버 지도 시스템은 data-cid에 url 파라미터를 저장해두고 있었습니다.
#       # data-cid 번호를 뽑아두었다가 기본 url 템플릿에 넣어 최종적인 url을 완성하면 끝❗
  
#   except Exception as e1:
#       if "li:nth-child(1)" in str(e1):
#           try:
#               select_df.iloc[i,-1] =driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview")
#               time.sleep(1)
          
#           except Exception as e2:
#               print(e2)
#               select_df.iloc[i, -1] = np.nan
#               time.sleep(1)
      
#       else:
#           pass                    

# driver.quit()


# #이때 수집한 것은 완전한 url이 아니라 url에 들어갈 ID (data-cid 라는 코드명으로 저장된 것)이므로, 온전한 URL로 만들어 줍니다.
# select_df['naver_store_url'] = "https://m.place.naver.com/restaurant/" + select_df['naver_store_url']

# #url이 수집되지 않은 데이터는 제거해준다.
# select_df = select_df.loc[~select_df['naver_store_url'].isnull()]


# #수집한 데이터를 csv 형태로 내보냅니다.
# select_df.to_csv('c:/Users/j.park/Section3/real_project3/first_crawling.csv', index = False, encoding= 'cp949')



# # #------------------------------------------❗ 문제점 발견 ❗------------------------------------------------
# # 수집한 데이터를 csv형태로 복원하여 살펴보던 도중 문제점을 발견했습니다.
# # 가게의 주소와 조사된 행정동명이 다른 경우입니다. (Ex: 신정상회는 csv 파일에서는 괴안동에 위치하지만, 실제로 찾아보니 소사본동이었습니다.)
# # ❗❗❗애초에 공공데이터에서 가져온 데이터가 잘못된 경우입니다❗❗❗



# # #------------------------------------------🔰🔰🔰🔰🔰 PART. 3 🔰🔰🔰🔰🔰------------------------------------------------
# # # PART.2를 통해 수집한 상세페이지 url이  담긴 데이터를 확인합니다.
# # # 이후 홈페이지에서 활용할 수 있는 데이터들을 크롤링하도록 합니다.(마찬가지로, 셀레니움을 이용합니다.)

# def modified_data(df):
#   # 가게의 주소 및 별점을 가져오도록 합시다.
#   from selenium.webdriver.chrome.service import Service
#   from selenium.webdriver.common.by import B
  
#   # 크롤링을 진행할 셀레니움의 드라이버 경로를 지정합니다.
#   s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
  
#   # 드라이버를 저장합니다.(경로 이용)
#   driver = webdriver.Chrome(service=s)
  
#   # ✅df.column : naver_store_url 의 가게 url을 이용하여 데이터를 수집합니다.✅
#   # 우리가 음식점을 검색할 때 중요시하는 상황들은 무엇이 있을까요?🤔
  
  
#   # step 1. 가게의 주소를 가져와보도록 합시다.
#   store_address_list = []
  
#   for i, url in enumerate((df['naver_store_url'])):
    
#     # 드라이버에 연결할 주소를 가져옵니다.
#     driver.get(url)

#     try:
#       #step 1: 가게의 '위도', '경도' 이외의 '주소'를 가져옵니다.
#       store_address = driver.find_element_by_css_selector('#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._1aj6- > div > a > span._2yqUQ').text
#       store_address_list.append(store_address)
    
#     except Exception as e1:
#       print(f'{i}행의 가게 주소를 찾을 수 없나봐요🤣')
#       store_address_list.append("null")
  
#   df['store_address'] = store_address_list
#   df.to_csv('c:/Users/j.park/Section3/real_project3/add_address.csv',index = False, encoding = 'cp949')
#   return None 


# df1 = pd.read_csv('first_crawling.csv', index =False, encoding='cp949')
# modified_data(df1)
      
  
  
  


