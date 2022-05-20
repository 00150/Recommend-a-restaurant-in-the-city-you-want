#0. 사용할 패키지 가져오기
from multiprocessing import connection
import pandas as pd
import numpy as np
import os
import sqlite3
import psycopg2
import csv
import logging


#1. 사용할 데이터의 경로 설정 및 데이터 가져오기.
data = os.path.join(os.getcwd(),'경기상권정보.csv')
df = pd.read_csv(data)


#2. 음식에 해당하는 데이터만 출력 및 사용할 컬럼만 지정하기.
df = df.loc[df['상권업종대분류명'] == '음식']

columns =['상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도']
df = df[columns]


#3. 입력하는 동을 기준으로, 원하는 데이터만 출력 및 따로 저장하기. 
# # ---> 함수를 생성하여 이용하겠습니다.
def mapping_address():
      #3-1. 찾고자 하는 동의 이름을 입력 받습니다.
  dong = input('찾고자하는 동네의 동 이름을 입력하세요😆 : ').replace(" ", '').split(',') # 은행2동, 장항2동, 와동
  dong_name = dong

  #3-2. 기본 데이터 생성
  default_data = pd.DataFrame(columns = {'상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도'})  

  #3-3. for문을 통해 기입한 동이름으로만 데이터를 따로 구성합니다.
  for number in range(len(dong_name)):
    add_df = df.loc[(df['행정동명'] == dong_name[number])]
    default_data = pd.concat([add_df, default_data])
  
  #3-4. 원하는 지역으로 구성된 데이터프레임을 따로 저장합니다.
  default_data.to_csv('c:/Users/j.park/Section3/real_project3/SELECT_REGION.csv', index = False, encoding= 'cp949')
  


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
    상권업종중분류명 VARCHAR(128),
    상권업종소분류명 VARCHAR(128),
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
        cur.execute("""INSERT INTO SELECT_REGION(Id, 상호명, 상권업종중분류명,
                              상권업종소분류명, 표준산업분류명, 행정동명, 위도, 경도) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
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

#(2). DB 연결
connect_sql()