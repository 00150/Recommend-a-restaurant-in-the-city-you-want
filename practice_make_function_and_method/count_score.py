#사용할 라이브러리를 불러옵니다.
from tkinter import EXCEPTION
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


#----평점평가에 참여한 인원을 크롤링하는 함수

def count_score_of_store(df):
    search_score_all_list = []
    default_comment = ""
    
    chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    
    for i, url in enumerate(df['naver_store_url']):
        driver.get(url +'/review/visitor')
        time.sleep(1)
        
        try:
            search_count_score_all = driver.find_elements(by=By.CLASS_NAME, value='ANYgl')
            for i in search_count_score_all:
                x = i.get_attribute('innerText')
                default_comment = default_comment +'/' + x 
            search_score_all_list.append(default_comment)
            default_comment = ""
        
        
        except Exception as e1: 
            print(f'{i} 행은 몇 명이 점수를 주었는지 알 수 없습니다.') 
            search_score_all_list.append('null')   
    
       
    driver.quit()
    df['total_of_people_voted'] = search_score_all_list 
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_total_count_voted.csv', index = False, encoding= 'utf-8')
    return None 


#---------------------한마디 남긴 총 인원수
def count_review_of_store(df):
    empty_list = []
    default_comment = ""
    
    chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    
    for i, url in enumerate(df['naver_store_url']):
        driver.get(url +'/review/visitor')
        time.sleep(1)
        
        try:
            collecting_reviews = driver.find_element(by=By.CLASS_NAME, value='place_section_count').text
            empty_list.append(collecting_reviews)
            
        except Exception as e1:
            print(f"{i} 행 가게에서 '인원 수'를 찾을 수 없습니다.")
            words = 'empty'
            empty_list.append(words)
    
    driver.quit()            
    df['리뷰 총인원'] = empty_list
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/add_comment_people_count.csv', index = False, encoding= 'utf-8')
    return None 
            









url = r'C:\Users\j.park\Section3\real_project3\create_csv\add_total_count_voted.csv'
df = pd.read_csv(url, encoding='utf-8')


count_review_of_store(df)