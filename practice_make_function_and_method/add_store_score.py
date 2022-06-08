# #------------------------------------------🔰🔰🔰🔰🔰 가게의 별점만을 크롤링하는 함수 생성 🔰🔰🔰🔰🔰------------------------------------------------
#사용할 라이브러리 가져오기.
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time


def add_store_score(df):
    #크롤링으로 가져올 점수를 저장할 빈 리스트를 생성합니다.
    store_score_list = []
      
    # 크롤링을 진행할 셀레니움의 드라이버 경로를 지정합니다.
    s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
  
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
    df.to_csv('c:/Users/j.park/Section3/real_project3/add_store_score.csv',index = False, encoding = 'cp949')
    return None 



df1 = pd.read_csv('add_address.csv', encoding='cp949')
add_store_score(df1)