import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time


# #------------------------------------------🔰🔰🔰🔰🔰 가게의 주소만을 크롤링하는 함수 생성 🔰🔰🔰🔰🔰------------------------------------------------


def modified_data(df):
  # 크롤링으로 찾은 가게의 주소를 저장할 빈 리스트를 생성합니다.
  store_address_list = []
  
  
  # 크롤링을 진행할 셀레니움의 드라이버 경로를 지정합니다.
  s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
  
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
  df.to_csv('c:/Users/j.park/Section3/real_project3/add_address.csv',index = False, encoding = 'cp949')
  return None 



# 🤩함수를 생성하였으므로, 데이터를 불러 함수를 사용하여 봅시다.

df1 = pd.read_csv('first_crawling.csv', encoding='cp949')
modified_data(df1)
 
 
 
 
 
 



     