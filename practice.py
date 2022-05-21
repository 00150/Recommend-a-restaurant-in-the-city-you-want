# # 1. 셀레니움 작동확인 완료
# import selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# driver =webdriver.Chrome()

# 2. 셀레니움 경로 작성하여 작동확인.(완료)

# import selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# driver = webdriver.Chrome(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')


#끄적끄적
import pandas as pd
df = pd.read_csv('SELECT_REGION.csv', encoding='cp949')

#🔆 셀레니움 : 사용할 라이브러리를 불러옵니다.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


# 셀레니움을 사용하기 위해 다운로드한 크롬 드라이버의 경로를 작성합니다. 
# ※ 현재 작업중에 있는 코드파일의 디렉토리에 함께 위치하는 것이 베스트인 것 같슴다..
chromedriver = r'C:\Users\j.park\Section3\real_project3\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)




# 크롤링으로 데이터를 얻어올 곳은 네이버로 진행하겠습니다.
# 네이버 지도 검색창에 [~동 ~~식당]으로 검색하여 정확도를 높혀줍니다. 검색어를 미리 설정하여줍시다.
df['네이버_키워드'] = df['행정동명'] + "%20" +df['행정동명'] #❗ "%20"은 띄어쓰기를 의미합니다.
df['naver_map_url'] = ''

# 본격적으로 가게 상세페이지의 URL을 가져오도록 합니다.

for i, keyword in enumerate(df['네이버_키워드'].tolist()):  #tolist를 이용, 객체 생성
    print("이번에 찾을 키워드는 다음과 같습니다 :", i, f'/{df.shape[0]-1}행', keyword) #csv 파일의 첫번째 행에 컬럼이 담겨있으므로 제외.
    
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
df['naver_map_url'] = "https://m.place.naver.com/restaurant/" + df['naver_map_url']

#url이 수집되지 않은 데이터는 제거해준다.
df = df.loc[~df['naver_map_url'].isnull()]