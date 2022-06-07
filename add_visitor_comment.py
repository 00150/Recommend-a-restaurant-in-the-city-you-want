import pandas as pd
import numpy as np
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service 
import time




# 방문객의 남긴 방문자 리뷰를 크롤링하여 봅시다. 
# ❗ 먼저 1개의 리뷰를 가져와보도록 합시다. ❗

def add_comment_only_one(df):
    
  # 드라이버의 주소를 설정합니다.
  s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
    
    
  # ❗오류수정 코드 : (오류내용) 시스템에 부착된 장치가 작동하지 않습니다. (0x1F)❗
  # 셀레니움 드라이브 옵션 수정
  # options = webdriver.ChromeOptions()
  # options.add_experimental_option("excludeSwitches", ["enable-logging"])
  # 위 옵션을 사용시 드라이버에 다음과 같은 파라미터를 넣어야 합니다.options=options
   
    
  #드라이버를 지정합니다, 이 때 수정한 옵션을 파라미터로 함께 지정해줍니다.
  comment_driver = webdriver.Chrome(service=s)
    
  #빈 리스트 1
  visitor_comment_list = []
   

  for i, url in enumerate(df['naver_store_url']):
              
    # 크롤링할 리뷰가 존재하는 url을 드라이버에 연결합니다.
    comment_driver.get(url+'/review/visitor?reviewItem=0')
    time.sleep(1)
    try:
      visitor_review = comment_driver.find_element_by_class_name("WoYOw").text
      visitor_comment_list.append(visitor_review)
    
    except Exception as e1:
      print(f'{i}행의 리뷰가 존재하지 않습니다.')
      visitor_review = 'None comment by visitor'
      visitor_comment_list.append(visitor_review)

  comment_driver.quit()
  df['visitor_comment'] = visitor_comment_list
  df.to_csv('c:/Users/j.park/Section3/real_project3/add_visitor_comment.csv',index = False, encoding='utf-8')
  
  return None 


# --------------------🔱 생성된 함수를 실행하기 위해선 다음과 같은 코드를 실행해야 합니다. 🔱------------------------

df1 = pd.read_csv('add_store_score.csv', encoding='cp949')
add_comment_only_one(df1)



#-------------------- 🔰 part2.  🔰 ------------------------
#이번에는 모든 리뷰를 가져올 수 있게 시도하여 봅시다.


# df1 = pd.read_csv('add_store_score.csv', encoding='cp949')
# # 셀레니움 드라이브 연결
# s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
# comment_driver = webdriver.Chrome(service=s)

# # 크롤링한 데이터를 모으기 위한 빈 리스트 생성
# visitor_comment_list = []


# # 임시 저장소
# temporary_list = []

# #df_column : df['naver_store_url'] 이용
# for i, url in enumerate(df1['naver_store_url']):
          
#   # 크롤링할 리뷰가 존재하는 url을 드라이버에 연결합니다.
#   comment_driver.get(url+'/review/visitor?reviewItem=0')
#   #try:
  
#     #전체 리뷰 텍스트 가져오기
#     #참고 : find_elements_by 로 가져오는 내용은 리스트로 저장됩니다. 
#   visitor_review =temporary_list.append(comment_driver.find_elements_by_class_name("WoYOw"))

# breakpoint()    
#     for elements in visitor_review:
#       reviews = ','.join(elements)
#       visitor_comment_list.append(reviews)


#   except Exception as e1:
#     print(f'{i}행의 리뷰가 존재하지 않습니다.')
#     visitor_review = 'None comment by visitor'
#     visitor_comment_list.append(visitor_review)

# comment_driver.quit()
# df1['all_review_by_visitor'] = visitor_comment_list

# return None



# df1 = pd.read_csv('add_store_score.csv', encoding='cp949')
# all_review_select(df1)
    
    
#app-root > div > div > div > div:nth-child(7) > div > div.place_section._3fSeV > div > ul > li:nth-child(1) > div.faZHB > a > span  
#app-root > div > div > div > div:nth-child(7) > div > div.place_section._3fSeV > div > ul > li:nth-child(2) > div.faZHB > a > span





