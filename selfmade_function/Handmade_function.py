# 🔰 직접 생성한 함수.  '크롤링 : 셀레니움', "db"




#사용할 라이브러리를 불러옵니다.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time

import pandas as pd
import numpy as np
import csv
import os
import sqlite3
import psycopg2
import logging



# 셀레니움에 이용할 크롬 드라이버의 경로를 작성합니다.
# ※ 현재 작업중에 있는 코드파일의 디렉토리에 함께 위치하는 것이 좋습니다.
chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

# ✅ 다음은 셀레니움을 활용하여 각기 다른 부분을 크롤링한 뒤 데이터를 조합하는 함수를 생성합니다. ✅





#--------------- 📜 part1. 가게의 url을 컬럼으로 저장하는 함수를 생성합니다.---------------------------


def add_url_column(df):
    for i, keyword in enumerate(df['네이버키워드'].tolist()):  #tolist를 이용, 객체 생성
        print("이번에 찾을 키워드는 다음과 같습니다 :", i, f'/{df.shape[0]-1}행', keyword) 
        
        try:
            naver_map_search_url = f'https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5'  # 현재 주소는 모바일입니다.
            driver.get(naver_map_search_url)    
            time.sleep(3.5)    
            df.iloc[i,-1] = driver.find_element_by_css_selector(
                '#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview').get_attribute('data-cid')
                # 네이버 지도 시스템은 data-cid에 url 파라미터를 저장해두고 있었습니다.
                # data-cid 번호를 뽑아두었다가 기본 url 템플릿에 넣어 최종적인 url을 완성하면 끝❗
        
        
        except Exception as e1:
        
            if "li:nth-child(1)" in str(e1):
                try:
                    df.iloc[i,-1] =driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview")
                    time.sleep(1)
          
                except Exception as e2:
                    print(e2)
                    df.iloc[i, -1] = np.nan
                    time.sleep(1)

            else:
                pass
    
    driver.quit()
    
    #이때 수집한 것은 완전한 url이 아니라 url에 들어갈 ID (data-cid 라는 코드명으로 저장된 것)이므로, 온전한 URL로 만들어 줍니다.
    df['naver_store_url'] = "https://m.place.naver.com/restaurant/" + df['naver_store_url']

    #url이 수집되지 않은 데이터는 제거해준다.
    df = df.loc[~df['naver_store_url'].isnull()]


    #수집한 데이터를 csv 형태로 내보냅니다.
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_url.csv', index = False, encoding= 'cp949')

    return None



#--------------- 📜 part2. 가게의 주소를 크롤링하는 함수를 생성합니다.---------------------------
# 참고 +) 가게의 '위도', '경도' 이외의 '주소'를 가져옵니다.


def add_address(df):
  # 크롤링으로 찾은 가게의 주소를 저장할 빈 리스트를 생성합니다.
  store_address_list = []
  
  
  # 크롤링을 진행할 셀레니움의 드라이버 경로를 지정합니다.
  s = Service(r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe')
  
  # 드라이버
  driver = webdriver.Chrome(service=s)
  # ✅df.column : naver_store_url 의 가게 url을 이용하여 데이터를 수집합니다.✅
  # 우리가 음식점을 검색할 때 중요시하는 상황들은 무엇이 있을까요?🤔
  
  for i, url in enumerate(df['naver_store_url']):
      driver.get(url+'/home/location?subtab=location')
      time.sleep(1)
      
      try:
          # 가게의 주소를 가져옵니다.
          store_address = driver.find_element_by_css_selector('#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._1aj6- > div > a > span._2yqUQ').text
          store_address_list.append(store_address)
      
      except Exception as e1:
          print(f'{i} 행의 주소를 가져올 수 없습니다..') 
          store_address_list.append('null')   
      
  driver.quit()            
  df['store_address'] = store_address_list
  df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_url_address.csv', index = False, encoding= 'cp949')
  return None 




#--------------- 📜 part3. 가게의 평점을 크롤링하는 함수를 생성합니다.---------------------------



def add_store_score(df):
    #크롤링으로 가져올 점수를 저장할 빈 리스트를 생성합니다.
    store_score_list = []
      
    # 크롤링을 진행할 셀레니움의 드라이버 경로를 지정합니다.
    s = Service(r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe')
  
    # 드라이버
    score_driver = webdriver.Chrome(service=s)
    # ✅df.column : naver_store_url 의 가게 url을 이용하여 데이터를 수집합니다.✅
    # 우리가 음식점을 검색할 때 중요시하는 상황들은 무엇이 있을까요?🤔
  
  
    for i, url in enumerate(df['naver_store_url']):
        score_driver.get(url)
        time.sleep(1)
        try:
            # 가게의 평점을 가져옵니다.
            store_score = score_driver.find_element_by_css_selector('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd > div._20Ivz > span._1Y6hi._1A8_M > em').text
            store_score_list.append(store_score)
      
        except Exception as e1:
            print(f'{i} 행의 점수를 가져올 수 없습니다..') 
            store_score_list.append('null')   
      
    score_driver.quit()            
    df['store_score'] = store_score_list
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_url_address_score.csv', index = False, encoding= 'cp949')
    return None 



#--------------- 📜 part4. 가게의 리뷰를 크롤링하는 함수를 생성합니다.---------------------------


def add_review_text(df):

    #기본값
    default_comment = ''

    comment_house = []

    chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)


    for i, url in enumerate(df['naver_store_url']):
        
        driver.get(url +'/review/visitor')
        time.sleep(1)
        
        try:
            search_review = driver.find_elements(by=By.CLASS_NAME, value= "WoYOw")
            for comment in search_review:
                x = comment.get_attribute('innerText')
                default_comment = default_comment +'/' + x  
            comment_house.append(default_comment)
            default_comment = ''

            
        except Exception as e1 :
            print(f'{i}행에 리뷰가 존재하지 않음')
        
            ax = 'Null'
            comment_house.append(ax)    
        

    driver.quit()

    df['visitor_review'] = comment_house
    df_comment = df['visitor_review']
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_url_address_score_review.csv', index = False, encoding= 'utf-8')
    
    return None


#--------------- 📜 part5. 가게의 리뷰 점수에 참여한 총 인원수를 크롤링하는 함수를 생성합니다.---------------------------



def count_score_of_store(df):
    search_score_all_list = []
    default_comment = ""
    
    chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    
    for i, url in enumerate(df['naver_store_url']):
        driver.get(url +'/review/visitor')
        time.sleep(1)
        
        try:
            search_count_score_all = driver.find_elements(by=By.CLASS_NAME, value='ANYgl')
            for i in search_count_score_all:
                x = i.get_attribute('innerText')
                default_comment = default_comment +'/' + x 
            search_score_all_list.append(default_comment)
            default_comment = ""
        
        
        except Exception as e1: 
            print(f'{i} 행은 몇 명이 점수를 주었는지 알 수 없습니다.') 
            search_score_all_list.append('null')   
    
       
    driver.quit()
    df['total_of_people_voted'] = search_score_all_list 
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_total_count_voted.csv', index = False, encoding= 'utf-8')
    return None 



#--------------- 📜 part6. 가게의 텍스트리뷰에 참여한 총 인원수를 크롤링하는 함수를 생성합니다.---------------------------



def count_review_of_store(df):
    empty_list = []
    default_comment = ""
    
    chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    
    for i, url in enumerate(df['naver_store_url']):
        driver.get(url +'/review/visitor')
        time.sleep(1)
        
        try:
            collecting_reviews = driver.find_element(by=By.CLASS_NAME, value='place_section_count').text
            empty_list.append(collecting_reviews)
            
        except Exception as e1:
            print(f"{i} 행 가게에서 '인원 수'를 찾을 수 없습니다.")
            words = 'empty'
            empty_list.append(words)
    
    driver.quit()            
    df['리뷰 총인원'] = empty_list
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_comment_people_count.csv', index = False, encoding= 'utf-8')
    return None 
            



#-----------------------------------------------PART 2 : 데이터 나누기.

def dividing_data(df):
    location = df[['상호명','행정동명', '위도', '경도', '가게_주소']]
    property = df[['업종중분류명', '업종소분류명', '표준산업분류명','합친데이터']]
    online = df[['네이버키워드','가게_URL']]
    evaluation = df[['가게_평점','평점에_참여한_인원','방문자_리뷰', '리뷰_총인원']]

    return location, property, online, evaluation
#-----------------------------------------------PART 3 : 클라우드 데이터 서비스 연결


# 클라우드 데이터 서비스 연결 : ElephantSQL
#4. 이후 생성된 데이터를 클라우드 데이터 서비스에 저장하도록 합니다.
#   Postgre 데이터베이스 서버와 연결 -> 클라우드 데이터베이스에서 생성한 elephantDB를 대상으로 합니다.
#   데이터베이스에 연결할 때, 필요한 정보들을 사전에 변수에 담아 놓습니다.

# ❗❗❗ 완전히 정제된 데이터 cleaned_Data.csv 파일을 DB에 넣는 작업입니다.
#     완전히 정제된 cleaned_Data.csv 파일의 컬럼은 다음과 같습니다. 
#     상호명,업종중분류명,업종소분류명,표준산업분류명,행정동명,위도,경도,합친데이터,
#     네이버키워드,가게_URL,가게_주소,가게_평점,평점에_참여한_인원,방문자_리뷰,리뷰_총인원




#4-1. 연결 & 테이블 생성 & 테이블 삽입을 진행할 함수를 작성합니다.

def divided_data_insert_cloud():
    
    
    # 연결 및 에러 제어 
    host = 'castor.db.elephantsql.com'
    user = 'iejeegfa'
    password = 'qjLvYChc-r75m8BZoQFRgNzRWlhNfV4U'
    database = 'iejeegfa'
    
    try:
        connection = psycopg2.connect(
            host = host,
            user = user,
            database = database,
            password = password)
        cur = connection.cursor()
  
    except:
        logging.error("could not connect to rds")




    # 1. 테이블 생성 : location - 위치 관련 데이터를 담은 테이블.
    cur.execute("DROP TABLE IF EXISTS evaluation;")
    cur.execute("DROP TABLE IF EXISTS online;")
    cur.execute("DROP TABLE IF EXISTS property;")
    cur.execute("DROP TABLE location CASCADE;")
    cur.execute("DROP TABLE IF EXISTS location;")
    
    cur.execute("""CREATE TABLE location(
        Id INTEGER PRIMARY KEY,
        상호명 VARCHAR(128),
        행정동명 VARCHAR(128),
        위도 FLOAT8,
        경도 FLOAT8,
        가게_주소 VARCHAR(200)
        );""")
  
    # 데이터 삽입.  
    # 적용될 csv 파일의 위치 지정   
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\location.csv'
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for id, row in enumerate(reader, start=1):
                cur.execute("""INSERT INTO location(Id, 상호명,행정동명, 위도, 경도, 가게_주소) VALUES (%s, %s, %s, %s, %s, %s);""",
                            (id, row[0],row[1], row[2], row[3], row[4]))
            print('making table : location mission complete❗')      
    
        except:
            logging.error("can't insert data")   


  
    # 2. 테이블 생성 : property - 판매 업종 관련 데이터를 담은 테이블.
    cur.execute("DROP TABLE IF EXISTS property;")
    cur.execute("""CREATE TABLE property(
        Id INTEGER PRIMARY KEY,
        업종중분류명 VARCHAR(128),
        업종소분류명 VARCHAR(128),
        표준산업분류명 VARCHAR(128),
        합친데이터 VARCHAR(128),
        FOREIGN KEY(Id) REFERENCES location(Id)
        );""")
  
    # 데이터 삽입.  
    # 적용될 csv 파일의 위치 지정   
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\property.csv'
  
    with open(csv_file, 'r', encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for id, row in enumerate(reader, start=1):
                cur.execute("""INSERT INTO property(Id, 업종중분류명, 업종소분류명, 표준산업분류명, 합친데이터) VALUES (%s, %s, %s, %s, %s);""",
                            (id, row[0],row[1], row[2], row[3]))
            print('making table : property mission complete❗')      
    
        except:
            logging.error("can't insert data")


       
    # 3. 테이블 생성 : online - 가게 url 및 '네이버키워드' 를 담은 테이블.
    cur.execute("DROP TABLE IF EXISTS online;")
    cur.execute("""CREATE TABLE online(
        Id INTEGER PRIMARY KEY,
        네이버키워드 VARCHAR(128),
        가게_URL VARCHAR(128),
        FOREIGN KEY(Id) REFERENCES location(Id)
        );""")
  
    # 데이터 삽입.  
    # 적용될 csv 파일의 위치 지정   
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\online.csv'
    with open(csv_file, 'r',  encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for id, row in enumerate(reader, start=1):
                cur.execute("""INSERT INTO online(Id, 네이버키워드,가게_URL) VALUES (%s, %s, %s);""",
                            (id, row[0],row[1]))
            print('making table : online mission complete❗')      
    
        except:
            logging.error("can't insert data")   
    


    # 4. 테이블 생성 : evaluation - 가게 평가 관련 데이터를 담은 테이블
    cur.execute("DROP TABLE IF EXISTS evaluation;")
    cur.execute("""CREATE TABLE evaluation(
        Id INTEGER PRIMARY KEY,
        가게_평점 FLOAT8,
        평점에_참여한_인원 INTEGER,
        방문자_리뷰 VARCHAR(2048),
        리뷰_총인원 INTEGER,
        FOREIGN KEY(Id) REFERENCES location(Id)
        );""")
  
    # 데이터 삽입.  
    # 적용될 csv 파일의 위치 지정   
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\evaluation.csv'
  
    with open(csv_file, 'r',  encoding='utf-8') as f:
        #try:
        reader = csv.reader(f)
        next(reader)
        for id, row in enumerate(reader, start=1):
            cur.execute("""INSERT INTO evaluation(Id, 가게_평점, 평점에_참여한_인원, 방문자_리뷰, 리뷰_총인원) VALUES (%s, %s, %s, %s, %s);""",
                        (id, row[0],row[1], row[2], row[3]))


        print('making table : evaluation mission complete❗')      

        #except:
        #    logging.error("can't insert data")   
    

    connection.commit()
    connection.close() 
    
    return None



# --- elephant - sql 연결 코드---

def connect_sql():
    # ele-sql 연결 및 에러 제어 
    # 2개의 값을 리턴합니다.
    
    host = 'castor.db.elephantsql.com'
    user = 'iejeegfa'
    password = 'qjLvYChc-r75m8BZoQFRgNzRWlhNfV4U'
    database = 'iejeegfa'


    try:
        connection = psycopg2.connect(
            host = host,
            user = user,
            database = database,
            password = password)
        cur = connection.cursor()

    except:
        logging.error("could not connect to rds")
    
    return cur, connection