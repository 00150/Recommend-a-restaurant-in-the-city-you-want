# #------------------------------------------π°π°π°π°π° κ°κ²μ λ³μ λ§μ ν¬λ‘€λ§νλ ν¨μ μμ± π°π°π°π°π°------------------------------------------------
#μ¬μ©ν  λΌμ΄λΈλ¬λ¦¬ κ°μ Έμ€κΈ°.
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time


def add_store_score(df):
    #ν¬λ‘€λ§μΌλ‘ κ°μ Έμ¬ μ μλ₯Ό μ μ₯ν  λΉ λ¦¬μ€νΈλ₯Ό μμ±ν©λλ€.
    store_score_list = []
      
    # ν¬λ‘€λ§μ μ§νν  μλ λμμ λλΌμ΄λ² κ²½λ‘λ₯Ό μ§μ ν©λλ€.
    s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
  
    # λλΌμ΄λ²
    score_driver = webdriver.Chrome(service=s)
    # βdf.column : naver_store_url μ κ°κ² urlμ μ΄μ©νμ¬ λ°μ΄ν°λ₯Ό μμ§ν©λλ€.β
    # μ°λ¦¬κ° μμμ μ κ²μν  λ μ€μμνλ μν©λ€μ λ¬΄μμ΄ μμκΉμ?π€
  
  
    for i, url in enumerate(df['naver_store_url']):
        score_driver.get(url)
        time.sleep(1)
        try:
            # κ°κ²μ νμ μ κ°μ Έμ΅λλ€.
            store_score = score_driver.find_element_by_css_selector('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd > div._20Ivz > span._1Y6hi._1A8_M > em').text
            store_score_list.append(store_score)
      
        except Exception as e1:
            print(f'{i} νμ μ μλ₯Ό κ°μ Έμ¬ μ μμ΅λλ€..') 
            store_score_list.append('null')   
      
    score_driver.quit()            
    df['store_score'] = store_score_list
    df.to_csv('c:/Users/j.park/Section3/real_project3/add_store_score.csv',index = False, encoding = 'cp949')
    return None 



df1 = pd.read_csv('add_address.csv', encoding='cp949')
add_store_score(df1)