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


# #끄적끄적
# import pandas as pd
# df = pd.read_csv('SELECT_REGION.csv', encoding='cp949')

# #🔆 셀레니움 : 사용할 라이브러리를 불러옵니다.
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# import time


# # 셀레니움을 사용하기 위해 다운로드한 크롬 드라이버의 경로를 작성합니다. 
# # ※ 현재 작업중에 있는 코드파일의 디렉토리에 함께 위치하는 것이 베스트인 것 같슴다..
# chromedriver = r'C:\Users\j.park\Section3\real_project3\chromedriver.exe'
# driver = webdriver.Chrome(chromedriver)




# # 크롤링으로 데이터를 얻어올 곳은 네이버로 진행하겠습니다.
# # 네이버 지도 검색창에 [~동 ~~식당]으로 검색하여 정확도를 높혀줍니다. 검색어를 미리 설정하여줍시다.
# df['네이버_키워드'] = df['행정동명'] + "%20" +df['행정동명'] #❗ "%20"은 띄어쓰기를 의미합니다.
# df['naver_map_url'] = ''

# # 본격적으로 가게 상세페이지의 URL을 가져오도록 합니다.

# for i, keyword in enumerate(df['네이버_키워드'].tolist()):  #tolist를 이용, 객체 생성
#     print("이번에 찾을 키워드는 다음과 같습니다 :", i, f'/{df.shape[0]-1}행', keyword) #csv 파일의 첫번째 행에 컬럼이 담겨있으므로 제외.
    
#     try:
#         naver_map_search_url = f'https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5'  # 현재 주소는 모바일입니다.
#         driver.get(naver_map_search_url)    
#         time.sleep(3.5)    
#         df.iloc[i,-1] = driver.find_element_by_css_selector(
#             '#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview').get_attribute('data-cid')
#         # 네이버 지도 시스템은 data-cid에 url 파라미터를 저장해두고 있었습니다.
#         # data-cid 번호를 뽑아두었다가 기본 url 템플릿에 넣어 최종적인 url을 완성하면 끝❗
    
#     except Exception as e1:
#         if "li:nth-child(1)" in str(e1):
#             try:
#                 df.iloc[i,-1] =driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview")
#                 time.sleep(1)
            
#             except Exception as e2:
#                 print(e2)
#                 df.iloc[i, -1] = np.nan
#                 time.sleep(1)
        
#         else:
#             pass                    

# driver.quit()


# #이때 수집한 것은 완전한 url이 아니라 url에 들어갈 ID (data-cid 라는 코드명으로 저장된 것)이므로, 온전한 URL로 만들어 줍니다.
# df['naver_map_url'] = "https://m.place.naver.com/restaurant/" + df['naver_map_url']

# #url이 수집되지 않은 데이터는 제거해준다.
# df = df.loc[~df['naver_map_url'].isnull()]


# 패키지 추가 : tqdm  (패키지 사용전 설치 필수 입니다.)


from tqdm.notebook import tqdm

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
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

naver_store_name_type = []  
blog_review_list = []
blog_review_count_list = []
naver_star_review_list = []
naver_visitor_review_list = []


s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')

# 메인 드라이버 : 별점등을 크롤링
driver = webdriver.Chrome(service=s)

# 서브 드라이버 : 블로그 리뷰 텍스트를 리뷰 탭에 들어가서 크롤링
sub_driver = webdriver.Chrome(service=s)


# Part.2 에서 크롤링하여 모은 데이터를 가져옵니다.
crawling_df = pd.read_csv('first_crawling.csv', encoding= 'cp949')


def second_crawling(df_column):
  for i, url in enumerate(tqdm(df_column)): #tqdm : 작업 과정의 진행상황을 살펴볼 수 있습니다. 
    driver.get(url)
    sub_driver.get(url+"/review/urgc")
    time.sleep(2)
  
    try:
      
      # 간단한 정보 가져오기.
      
      # 가게의 유형 분류
      naver_store_type = driver.find_element_by_css_selector("#_title > span._3ocDE").text
      
      # 블로그 리뷰 수
      blog_review_count = driver.find_element_by_css_selector('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd > div._37n49 > span:nth-child(3) > a > em').text
      
      # 방문자 리뷰 수
      visitor_review_count = driver.find_element_by_css_selector("#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd > div._37n49 > span:nth-child(2) > a > em").text
      
      #가게 별점 점수
      review_stars = driver.find_element_by_css_selector("#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd > div._37n49 > span._1Y6hi._1A8_M > em").text

      # 리뷰 텍스트 가져오기.
      review_text_list = [] # 임시 선언
      
      # 네이버 지도 블로그 리뷰 탭
      # 동적 웹사이트의 순서가 주문하기, 메뉴보기 등의 존재 여부로 다르기 때문에 css selector가 아니라 element 찾기로 진행한다.
      # 즉 리뷰탭의 요소를 작성한다.
      review_text_crawl_list = sub_driver.find_elements_by_class_name("_3Q5_9")
      
      
      # find_elements_by_class_name 메소드를 통해  가져온 내용은 리스트로 저장된다.
      # 리스트 타입을 풀어서 임시 데이터에 모아 두어야 한다.(for문 사용)
      for review_crawing_data in review_text_crawl_list:
        
        # 임시로 선언된 review_text_list에 담기.
        review_text_list.append(review_crawing_data.find_element_by_tag_name("WoYOw").text)
      
      #리스트에 저장된 텍스트(한 식당에 대한 여러 리뷰들)를 덩어리로 모아줍니다.
      review_text = ",".join(review_text_list)
      
      
      blog_review_list.append(review_text)
      naver_store_name_type.append(naver_store_type)  
      blog_review_count_list.append(blog_review_count)
      naver_star_review_list.append(review_stars)
      naver_visitor_review_list.append(visitor_review_count)
      
    # 리뷰가 없는 업체는 크롤링에 오류가 뜨므로 정리할 것. 
    except Exception as e1:
      print(f'{i}행에 문제가 발생')
      
      #리뷰가 없으므로  null을 임시로 넣어준다.
      blog_review_list.append('null')
      naver_store_name_type.append('null')
      blog_review_count_list.append('null')
      naver_star_review_list.append('null')
      naver_visitor_review_list.append('null')
      
  driver.quit()
  sub_driver.quit()
  
  df['naver_store_type'] = naver_store_name_type
  df['naver_star_point'] = naver_star_review_list
  df['naver_blog_review_count'] = blog_review_count_list
  df['naver_blog_review_text'] = blog_review_list
  df['naver_visitor_review_count'] = naver_visitor_review_list
  
  #수집한 데이터를 csv 형태로 내보냅니다.
  df.to_csv('c:/Users/j.park/Section3/real_project3/second_crawling.csv', index = False, encoding= 'cp949')
  
  print('mission complete❗') 
  return None


#test_second_crawling
#실행해보고, 오류가 난다면 고쳐봅시다.
second_crawling(crawling_df['naver_map_url'])