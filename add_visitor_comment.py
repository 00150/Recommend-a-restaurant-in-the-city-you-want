import pandas as pd
import numpy as np
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service 
import time




# 방문객의 남긴 방문자 리뷰를 크롤링하여 봅시다. 
# ❗리뷰를 총 3개 가져오는 것이 목표 입니다❗

def add_comment(df):
    
    # 드라이버의 주소를 설정합니다.
    s = Service(r'C:\Users\j.park\Section3\real_project3\chromedriver.exe')
    
    
    # ❗오류수정 코드 : (오류내용) 시스템에 부착된 장치가 작동하지 않습니다. (0x1F)❗
    # 셀레니움 드라이브 옵션 수정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    #드라이버를 지정합니다, 이 때 수정한 옵션을 파라미터로 함께 지정해줍니다.
    comment_driver = webdriver.Chrome(service=s, options=options)
    
    #방문자 리뷰가 담길 빈 리스트를 생성합니다. 마지막 데이터프레임에 합쳐질 내용입니다.
    visitor_comment_list = []
    
    #처음 리뷰 텍스트를 지정합니다.
    review_text = ""
    
    for i, url in enumerate(df['naver_store_url']):
        
        # 크롤링할 리뷰가 존재하는 url을 드라이버에 연결합니다.
        comment_driver.get(url+'review/visitor?reviewItem=0')
        time.sleep(1)
        
        
        #방문자들이 남긴 리뷰들은 같은 클래스 : class = 'WoYOw' 로 묶여있으며, 이때 li:nth-child(num)의 num에 따라 위치하는 리뷰코멘트가 다릅니다.
        #app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section._3fSeV > div > ul > li:nth-child(1) > div.faZHB > a > span
        #app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section._3fSeV > div > ul > li:nth-child(2) > div.faZHB > a > span
        
        # 각 가게당 매겨진 리뷰 3개를 가져오려고 합니다.
        # 방문자 리뷰에서 처음에 위치한 리뷰의 순서는 1로 지정되었음을 확인할 수 있습니다. => li:nth-child(1) 
        # 처음에 시작하는 숫자 또한 0으로 지정합니다. 이후 구문에서 값을 더해줍니다.
        
        num = 0
        try:
            #while 문 동안 총 3번의 리뷰를 수집해야합니다.
            while num!=3:
                
                # 루프가 돌 수 있도록 숫자를 더해줍니다.
                num +=1
                
                # 리뷰를 수집하기 위한 코드를 작성합니다.
                a = comment_driver.find_element_by_css_selector(f'#app-root > div > div > div > div:nth-child(7) > div > div:nth-child(2) > div > div._32ycQ > ul > li:nth-child({num}) > div > div > div._2sQ0s > a > span').text    
                
                # 이후 수집된 리뷰를 일괄적으로 더해줍니다.
                review_text = review_text + "/" + a 
                
                # 이 때, 총 3개의 리뷰를 모두 수집했다면 결과를 다해줍니다.
                if num == 3:
                    visitor_comment_list.append(review_text)
        
        
        # 가게의 리뷰가 하나도 없을 때를 대비합니다.
        except Exception as e1:
            if "li:nth-child(1)" in str(e1):
                print(f"{i}행에 위치한 가게는 리뷰가 없네")
                
                #가게 리뷰가 없을 시, 집어넣을 문자열을 새성합니다.
                review_None_text = "empty"
                visitor_comment_list.append(review_None_text)
                break
            
            else:
                print(f"{i}행 문제가 발생 - 리뷰가 {num}개뿐이다")
                visitor_comment_list.append(review_text)
                break
    
    comment_driver.quit() 
    df['visitor_comment'] = visitor_comment_list
    df.to_csv('c:/Users/j.park/Section3/real_project3/add_visitor_comment.csv',index = False, encoding = 'cp949')
    return None                 

df1 = pd.read_csv('add_store_score.csv', encoding='cp949')
add_comment(df1)



                        
"""
실패했으나 대충 감이 왔다.

num = 0
empty_comment = ""
empty_list = []
try:
  while num!=3:
    num += 1
    empty_comment = empty_comment+ "/" + f'현재 숫자는 {num} 입니다.'
    if num == 3:
      empty_list.append(empty_comment)
except Exception as e1:
  print('oh')


❗실행결과❗
empty_list의 값은 다음과 같습니다.
['/현재 숫자는 1 입니다./현재 숫자는 2 입니다./현재 숫자는 3 입니다.']
⬆⬆⬆⬆⬆ ㅅㅂ 이걸 구현해야함 ㅇㅋㅂㄹ?

"""      
            
            
            

