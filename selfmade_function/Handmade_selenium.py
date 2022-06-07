# 셀레니움을 이용하여 크롤링합니다.


#❗ 함수 패키지를 따로 만들어 사용해보고자 합니다.
#❗ 셀리니움:드라이버를 이용하여 어떤 부분을 크롤링할 지 함수를 직접 생성하여 봅시다.


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


def modified_data(df):
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
    #크롤링으로 가져올 리뷰를 저장할 빈 리스트를 생성합니다.
    comment_house = []
    
    #comment의 기본 값은 다음과 같습니다.
    default_comment = ''
      
    # 크롤링을 진행할 셀레니움의 드라이버 경로를 지정합니다.
    s = Service(r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe')
    
    # 드라이버
    review_driver = webdriver.Chrome(service=s)
    
    for i, url in enumerate(df['naver_store_url']):
        review_driver.get(url +'/review/visitor')
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
    
    review_driver.quit()
    df['visitor_review'] = comment_house
    df_comment = df['visitor_review']
    df.to_csv('c:/Users/j.park/practice/selenium_practice/crawling_completed.csv',index = False, encoding='utf-8')
    
    return None