# 정제된 데이터 Cleaned_Data.csv 를 분할합니다.
# 분할된 데이터는 csv_divide 에 저장합니다.

import pandas as pd
import numpy as np
import csv
import os
import sqlite3
import psycopg2
import logging

url = r'C:\Users\j.park\Section3\real_project3\create_csv\cleaned_Data.csv'
df = pd.read_csv(url,encoding='utf-8')


def dividing_data(df):

    # 데이터 분할
    # 각각 연관된 컬럼별로 데이터를 합쳐 총 4개의 df 생성.
            #   1. location - 위치 관련 데이터를 담은 테이블  
            #   2. property - 판매 업종 관련 데이터를 담은 테이블
            #   3. online - 가게 url 및 '네이버키워드' 를 담은 테이블
            #   4. evaluation -평가 관련 데이터를 담은 테이블
            

    location = df[['상호명','행정동명', '위도', '경도', '가게_주소']]
    property = df[['업종중분류명', '업종소분류명', '표준산업분류명','합친데이터']]
    online = df[['네이버키워드','가게_URL']]
    evaluation = df[['가게_평점','평점에_참여한_인원','방문자_리뷰', '리뷰_총인원']]
    
    
    # 데이터 방출
    location.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/csv_divide/location.csv', index = False, encoding= 'utf-8')
    property.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/csv_divide/property.csv', index = False, encoding= 'utf-8')
    online.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/csv_divide/online.csv', index = False, encoding= 'utf-8')
    evaluation.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/csv_divide/evaluation.csv', index = False, encoding= 'utf-8')
    
    print('completed divide data')
        
    
    return None


dividing_data(df)


