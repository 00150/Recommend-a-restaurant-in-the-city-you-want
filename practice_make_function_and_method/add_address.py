import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time


# #------------------------------------------π°π°π°π°π° κ°κ²μ μ£Όμλ§μ ν¬λ‘€λ§νλ ν¨μ μμ± π°π°π°π°π°------------------------------------------------


def modified_data(df):
  # ν¬λ‘€λ§μΌλ‘ μ°Ύμ κ°κ²μ μ£Όμλ₯Ό μ μ₯ν  λΉ λ¦¬μ€νΈλ₯Ό μμ±ν©λλ€.
  store_address_list = []
  
  
  # ν¬λ‘€λ§μ μ§νν  μλ λμμ λλΌμ΄λ² κ²½λ‘λ₯Ό μ§μ ν©λλ€.
  s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
  
  # λλΌμ΄λ²
  driver = webdriver.Chrome(service=s)
  # βdf.column : naver_store_url μ κ°κ² urlμ μ΄μ©νμ¬ λ°μ΄ν°λ₯Ό μμ§ν©λλ€.β
  # μ°λ¦¬κ° μμμ μ κ²μν  λ μ€μμνλ μν©λ€μ λ¬΄μμ΄ μμκΉμ?π€
  
  for i, url in enumerate(df['naver_store_url']):
      driver.get(url+'/home/location?subtab=location')
      time.sleep(1)
      
      try:
          # κ°κ²μ μ£Όμλ₯Ό κ°μ Έμ΅λλ€.
          store_address = driver.find_element_by_css_selector('#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._1aj6- > div > a > span._2yqUQ').text
          store_address_list.append(store_address)
      
      except Exception as e1:
          print(f'{i} νμ μ£Όμλ₯Ό κ°μ Έμ¬ μ μμ΅λλ€..') 
          store_address_list.append('null')   
      
  driver.quit()            
  df['store_address'] = store_address_list
  df.to_csv('c:/Users/j.park/Section3/real_project3/add_address.csv',index = False, encoding = 'cp949')
  return None 



# π€©ν¨μλ₯Ό μμ±νμμΌλ―λ‘, λ°μ΄ν°λ₯Ό λΆλ¬ ν¨μλ₯Ό μ¬μ©νμ¬ λ΄μλ€.

df1 = pd.read_csv('first_crawling.csv', encoding='cp949')
modified_data(df1)
 
 
 
 
 
 



     