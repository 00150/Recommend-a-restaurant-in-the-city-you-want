#❗감정분석에 사용될  train 샘플 데이터를 만들고 있습니다.❗
# 만들어지는 csv 파일은 create_csv/traindata에 담겨있으니 확인바랍니다.
# Handmade_function.py로 생성된 함수 또한 경로가 위에 언급한 위치로 바뀌었으니, 확인바랍니다.


from selfmade_function import Handmade_function as Hf
import pandas as pd
import numpy as np
import csv
import os


url = r'C:\Users\j.park\Section3\real_project3\create_csv\traindata\SELECT_REGION.csv'
select_df =pd.read_csv(url, encoding='cp949')



# 만든 함수는 다음과 같습니다.
"""
📜 part1. 가게의 url을 컬럼으로 저장하는 함수를 생성
add_url_column(df) / return None / csv 파일 반환 (add_url.csv)


📜 part2. 가게의 주소를 크롤링하는 함수
add_address(df) / return None / csv 파일 반환 (add_url_address.csv)


📜 part3. 가게의 평점을 크롤링하는 함수
add_store_score(df) / return None / csv 파일 반환 (add_url_address_score.csv)


📜 part4. 가게의 리뷰를 크롤링하는 함수
add_review_text(df)  / return None / csv 파일 반환 (add_url_address_score_review.csv)


📜 part5. 평점평가에 참여한 인원을 크롤링하는 함수
count_score_of_store(df) return /csv 파일 반환 (add_total_count_voted.csv)


📜 part6. 리뷰에 참여한 인원을 크롤링하는 함수
count_score_of_store(df) return /csv 파일 반환 (add_comment_people_count.csv)
"""



# # 크롤링으로 데이터를 얻어올 곳은 네이버로 진행하겠습니다.
# # 네이버 지도 검색창에 [~동 ~~식당]으로 검색하여 정확도를 높혀줍니다. 검색어를 미리 설정하여줍시다.

select_df['네이버키워드'] = select_df['행정동명'] + "%20" + select_df['상호명']  #❗ "%20"은 띄어쓰기를 의미합니다.
select_df['naver_store_url'] = ''

# 이후, 함수를 사용합니다.
# 가게의 url을 컬럼으로 생성합니다.

# #📜 part1. 가게의 url을 컬럼으로 저장하는 함수를 생성
# Hf.add_url_column(select_df)


# #📜 part2. 가게의 주소를 크롤링하는 함수
# scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\traindata\add_url.csv'
# df1 = pd.read_csv(scv_url, encoding= 'cp949')
# Hf.add_address(df1)


# #📜 part3. 가게의 평점을 크롤링하는 함수
# scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\traindata\add_url_address.csv'
# df2 = pd.read_csv(scv_url, encoding= 'cp949')
# Hf.add_store_score(df2)


#📜 part4. 가게의 리뷰를 크롤링하는 함수
scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\traindata\add_url_address_score.csv'
df3 = pd.read_csv(scv_url, encoding= 'cp949')
Hf.add_review_text(df3)


# #📜 part5. 평점평가에 참여한 인원을 크롤링하는 함수
# scv_url = r'C:\Users\j.park\Section3\real_project3\create_csv\traindata\add_url_address_score_review.csv'
# df4 = pd.read_csv(scv_url, encoding= 'utf-8')
# Hf.count_score_of_store(df4)


# #📜 part6. 리뷰에 참여한 인원을 크롤링하는 함수
# scv_url =r'C:\Users\j.park\Section3\real_project3\create_csv\traindata\add_total_count_voted.csv'
# df5 = pd.read_csv(scv_url, encoding= 'cp949')
# Hf.count_review_of_store(df5)


