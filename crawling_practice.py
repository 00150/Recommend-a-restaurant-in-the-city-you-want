#. 데이터 불러오기.=
import pandas as pd
import numpy as np
df = pd.read_csv('first_crawling.csv', encoding='cp949')

#. 간격유지 위한 time 가져오기.
import time

#. 셀레니움 패키지 가져오기.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#진행상황을 알기 위해 tqdm 패키지 가져오기 (주피터 깔려있어야 함, 없다면 설치)
from tqdm.notebook import tqdm 


# ❗❗ 참고 : 셀레니움의 버전이 4로 업그레이드 되면서 쓰는 방법이 살짝 달라졌음
# # https://velog.io/@woonmong/DeprecationWarning-executablepath-has-been-deprecated-please-pass-in-a-Service-object-%EC%98%A4%EB%A5%98-%ED%95%B4%EA%B2%B0

# 경로 넣어주기, 이후 드라이버 설정.
s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')

# 메인 드라이버 : 별점등을 크롤링
driver = webdriver.Chrome(service=s)

#❗아직은 시도하지 않습니다.❗ 서브 드라이버 : 블로그 리뷰 텍스트를 리뷰 탭에 들어가서 크롤링
#❗아직은 시도하지 않습니다.❗ sub_driver = webdriver.Chrome(service=s)


#1.   데이터 first_crawling.csv 에서 df['naver_map_url']는 각 가게의 모바일 주소를 나타내고 있음.
#1-1. 먼저 각 가게의 평점을 가져와봅시다.

store_average_score = []

#for 문 이용.
for i, url in enumerate(tqdm(df['naver_map_url'])):
    driver.get(url)
    time.sleep(2)
    
    try:
        # 해당하는 selector 요소를 '해당 홈페이지 개발자 도구'에서 확인합니다.
        store_score = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section._11ptV > div > div > div._2oZg_ > span._1fvo3.Sv1wj > em").text
        store_average_score.append(store_score)
        
    # 별점이 없을 경우, 대안을 제시합니다.
    except Exception as e1:
        
        print(f'{i}행에 문제가 발생')
        store_average_score.append('null')  


driver.quit()    

df['store_average_score'] = store_average_score

    

