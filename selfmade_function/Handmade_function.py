# π° μ§μ  μμ±ν ν¨μ.  'ν¬λ‘€λ§ : μλ λμ', "db"
#β 6/30 κΈ°μ€μΌλ‘ νλ ¨ λ°μ΄ν°λ₯Ό μμ±ν©λλ€. csvλ₯Ό λ΄λ³΄λ΄λ μμΉκ° λ°λμμΌλ, νμΈλ°λλλ€.
#β traindata ν΄λλ‘ csv νμΌμ κ²½λ‘κ° μμ λμμ΅λλ€.




#μ¬μ©ν  λΌμ΄λΈλ¬λ¦¬λ₯Ό λΆλ¬μ΅λλ€.
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
import os
import sqlite3
import psycopg2
import logging



# μλ λμμ μ΄μ©ν  ν¬λ‘¬ λλΌμ΄λ²μ κ²½λ‘λ₯Ό μμ±ν©λλ€.
# β» νμ¬ μμμ€μ μλ μ½λνμΌμ λλ ν λ¦¬μ ν¨κ» μμΉνλ κ²μ΄ μ’μ΅λλ€.
chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

# β λ€μμ μλ λμμ νμ©νμ¬ κ°κΈ° λ€λ₯Έ λΆλΆμ ν¬λ‘€λ§ν λ€ λ°μ΄ν°λ₯Ό μ‘°ν©νλ ν¨μλ₯Ό μμ±ν©λλ€. β





#--------------- π part1. κ°κ²μ urlμ μ»¬λΌμΌλ‘ μ μ₯νλ ν¨μλ₯Ό μμ±ν©λλ€.---------------------------


def add_url_column(df):
    for i, keyword in enumerate(df['λ€μ΄λ²ν€μλ'].tolist()):  #tolistλ₯Ό μ΄μ©, κ°μ²΄ μμ±
        print("μ΄λ²μ μ°Ύμ ν€μλλ λ€μκ³Ό κ°μ΅λλ€ :", i, f'/{df.shape[0]-1}ν', keyword) 
        
        try:
            naver_map_search_url = f'https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5'  # νμ¬ μ£Όμλ λͺ¨λ°μΌμλλ€.
            driver.get(naver_map_search_url)    
            time.sleep(3.5)    
            df.iloc[i,-1] = driver.find_element_by_css_selector(
                '#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview').get_attribute('data-cid')
                # λ€μ΄λ² μ§λ μμ€νμ data-cidμ url νλΌλ―Έν°λ₯Ό μ μ₯ν΄λκ³  μμμ΅λλ€.
                # data-cid λ²νΈλ₯Ό λ½μλμλ€κ° κΈ°λ³Έ url ννλ¦Ώμ λ£μ΄ μ΅μ’μ μΈ urlμ μμ±νλ©΄ λβ
        
        
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
    
    #μ΄λ μμ§ν κ²μ μμ ν urlμ΄ μλλΌ urlμ λ€μ΄κ° ID (data-cid λΌλ μ½λλͺμΌλ‘ μ μ₯λ κ²)μ΄λ―λ‘, μ¨μ ν URLλ‘ λ§λ€μ΄ μ€λλ€.
    df['naver_store_url'] = "https://m.place.naver.com/restaurant/" + df['naver_store_url']

    #urlμ΄ μμ§λμ§ μμ λ°μ΄ν°λ μ κ±°ν΄μ€λ€.
    df = df.loc[~df['naver_store_url'].isnull()]


    #μμ§ν λ°μ΄ν°λ₯Ό csv ννλ‘ λ΄λ³΄λλλ€.
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/add_url.csv', index = False, encoding= 'cp949')

    return None



#--------------- π part2. κ°κ²μ μ£Όμλ₯Ό ν¬λ‘€λ§νλ ν¨μλ₯Ό μμ±ν©λλ€.---------------------------
# μ°Έκ³  +) κ°κ²μ 'μλ', 'κ²½λ' μ΄μΈμ 'μ£Όμ'λ₯Ό κ°μ Έμ΅λλ€.


def add_address(df):
  # ν¬λ‘€λ§μΌλ‘ μ°Ύμ κ°κ²μ μ£Όμλ₯Ό μ μ₯ν  λΉ λ¦¬μ€νΈλ₯Ό μμ±ν©λλ€.
  store_address_list = []
  
  
  # ν¬λ‘€λ§μ μ§νν  μλ λμμ λλΌμ΄λ² κ²½λ‘λ₯Ό μ§μ ν©λλ€.
  s = Service(r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe')
  
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
  df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/add_url_address.csv', index = False, encoding= 'cp949')
  return None 




#--------------- π part3. κ°κ²μ νμ μ ν¬λ‘€λ§νλ ν¨μλ₯Ό μμ±ν©λλ€.---------------------------



def add_store_score(df):
    #ν¬λ‘€λ§μΌλ‘ κ°μ Έμ¬ μ μλ₯Ό μ μ₯ν  λΉ λ¦¬μ€νΈλ₯Ό μμ±ν©λλ€.
    store_score_list = []
      
    # ν¬λ‘€λ§μ μ§νν  μλ λμμ λλΌμ΄λ² κ²½λ‘λ₯Ό μ§μ ν©λλ€.
    s = Service(r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe')
  
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
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/add_url_address_score.csv', index = False, encoding= 'cp949')
    return None 



#--------------- π part4. κ°κ²μ λ¦¬λ·°λ₯Ό ν¬λ‘€λ§νλ ν¨μλ₯Ό μμ±ν©λλ€.---------------------------


def add_review_text(df):

    #κΈ°λ³Έκ°
    default_comment = ''

    comment_house = []

    chromedriver = r'C:\Users\j.park\Section3\real_project3\selfmade_function\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)


    for i, url in enumerate(df['naver_store_url']):
        
        driver.get(url +'/review/visitor')
        time.sleep(1)
        
        try:
            search_review = driver.find_elements(by=By.CLASS_NAME, value= "WoYOw")
            for comment in search_review:
                x = comment.get_attribute('innerText')
                default_comment = default_comment +'/' + x  
            comment_house.append(default_comment)
            default_comment = ''

            
        except Exception as e1 :
            print(f'{i}νμ λ¦¬λ·°κ° μ‘΄μ¬νμ§ μμ')
        
            ax = 'Null'
            comment_house.append(ax)    
        

    driver.quit()

    df['visitor_review'] = comment_house
    df_comment = df['visitor_review']
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/add_url_address_score_review.csv', index = False, encoding= 'utf-8')
    
    return None


#--------------- π part5. κ°κ²μ λ¦¬λ·° μ μμ μ°Έμ¬ν μ΄ μΈμμλ₯Ό ν¬λ‘€λ§νλ ν¨μλ₯Ό μμ±ν©λλ€.---------------------------



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
            print(f'{i} νμ λͺ λͺμ΄ μ μλ₯Ό μ£Όμλμ§ μ μ μμ΅λλ€.') 
            search_score_all_list.append('null')   
    
       
    driver.quit()
    df['total_of_people_voted'] = search_score_all_list 
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/add_total_count_voted.csv', index = False, encoding= 'utf-8')
    return None 



#--------------- π part6. κ°κ²μ νμ€νΈλ¦¬λ·°μ μ°Έμ¬ν μ΄ μΈμμλ₯Ό ν¬λ‘€λ§νλ ν¨μλ₯Ό μμ±ν©λλ€.---------------------------



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
            print(f"{i} ν κ°κ²μμ 'μΈμ μ'λ₯Ό μ°Ύμ μ μμ΅λλ€.")
            words = 'empty'
            empty_list.append(words)
    
    driver.quit()            
    df['λ¦¬λ·° μ΄μΈμ'] = empty_list
    df.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/add_comment_people_count.csv', index = False, encoding= 'utf-8')
    return None 
            



#-----------------------------------------------PART 2 : λ°μ΄ν° λλκΈ°.

def dividing_data(df):
    location = df[['μνΈλͺ','νμ λλͺ', 'μλ', 'κ²½λ', 'κ°κ²_μ£Όμ']]
    property = df[['μμ’μ€λΆλ₯λͺ', 'μμ’μλΆλ₯λͺ', 'νμ€μ°μλΆλ₯λͺ','ν©μΉλ°μ΄ν°']]
    online = df[['λ€μ΄λ²ν€μλ','κ°κ²_URL']]
    evaluation = df[['κ°κ²_νμ ','νμ μ_μ°Έμ¬ν_μΈμ','λ°©λ¬Έμ_λ¦¬λ·°', 'λ¦¬λ·°_μ΄μΈμ']]

    return location, property, online, evaluation
#-----------------------------------------------PART 3 : ν΄λΌμ°λ λ°μ΄ν° μλΉμ€ μ°κ²°


# ν΄λΌμ°λ λ°μ΄ν° μλΉμ€ μ°κ²° : ElephantSQL
#4. μ΄ν μμ±λ λ°μ΄ν°λ₯Ό ν΄λΌμ°λ λ°μ΄ν° μλΉμ€μ μ μ₯νλλ‘ ν©λλ€.
#   Postgre λ°μ΄ν°λ² μ΄μ€ μλ²μ μ°κ²° -> ν΄λΌμ°λ λ°μ΄ν°λ² μ΄μ€μμ μμ±ν elephantDBλ₯Ό λμμΌλ‘ ν©λλ€.
#   λ°μ΄ν°λ² μ΄μ€μ μ°κ²°ν  λ, νμν μ λ³΄λ€μ μ¬μ μ λ³μμ λ΄μ λμ΅λλ€.

# βββ μμ ν μ μ λ λ°μ΄ν° cleaned_Data.csv νμΌμ DBμ λ£λ μμμλλ€.
#     μμ ν μ μ λ cleaned_Data.csv νμΌμ μ»¬λΌμ λ€μκ³Ό κ°μ΅λλ€. 
#     μνΈλͺ,μμ’μ€λΆλ₯λͺ,μμ’μλΆλ₯λͺ,νμ€μ°μλΆλ₯λͺ,νμ λλͺ,μλ,κ²½λ,ν©μΉλ°μ΄ν°,
#     λ€μ΄λ²ν€μλ,κ°κ²_URL,κ°κ²_μ£Όμ,κ°κ²_νμ ,νμ μ_μ°Έμ¬ν_μΈμ,λ°©λ¬Έμ_λ¦¬λ·°,λ¦¬λ·°_μ΄μΈμ




#4-1. μ°κ²° & νμ΄λΈ μμ± & νμ΄λΈ μ½μμ μ§νν  ν¨μλ₯Ό μμ±ν©λλ€.

def divided_data_insert_cloud():
    
    
    # μ°κ²° λ° μλ¬ μ μ΄ 
    host = 'castor.db.elephantsql.com'
    user = 'iejeegfa'
    password = 'qjLvYChc-r75m8BZoQFRgNzRWlhNfV4U'
    database = 'iejeegfa'
    
    try:
        connection = psycopg2.connect(
            host = host,
            user = user,
            database = database,
            password = password)
        cur = connection.cursor()
  
    except:
        logging.error("could not connect to rds")




    # 1. νμ΄λΈ μμ± : location - μμΉ κ΄λ ¨ λ°μ΄ν°λ₯Ό λ΄μ νμ΄λΈ.
    cur.execute("DROP TABLE IF EXISTS evaluation;")
    cur.execute("DROP TABLE IF EXISTS online;")
    cur.execute("DROP TABLE IF EXISTS property;")
    cur.execute("DROP TABLE location CASCADE;")
    cur.execute("DROP TABLE IF EXISTS location;")
    
    cur.execute("""CREATE TABLE location(
        Id INTEGER PRIMARY KEY,
        μνΈλͺ VARCHAR(128),
        νμ λλͺ VARCHAR(128),
        μλ FLOAT8,
        κ²½λ FLOAT8,
        κ°κ²_μ£Όμ VARCHAR(200)
        );""")
  
    # λ°μ΄ν° μ½μ.  
    # μ μ©λ  csv νμΌμ μμΉ μ§μ    
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\location.csv'
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for id, row in enumerate(reader, start=1):
                cur.execute("""INSERT INTO location(Id, μνΈλͺ,νμ λλͺ, μλ, κ²½λ, κ°κ²_μ£Όμ) VALUES (%s, %s, %s, %s, %s, %s);""",
                            (id, row[0],row[1], row[2], row[3], row[4]))
            print('making table : location mission completeβ')      
    
        except:
            logging.error("can't insert data")   


  
    # 2. νμ΄λΈ μμ± : property - νλ§€ μμ’ κ΄λ ¨ λ°μ΄ν°λ₯Ό λ΄μ νμ΄λΈ.
    cur.execute("DROP TABLE IF EXISTS property;")
    cur.execute("""CREATE TABLE property(
        Id INTEGER PRIMARY KEY,
        μμ’μ€λΆλ₯λͺ VARCHAR(128),
        μμ’μλΆλ₯λͺ VARCHAR(128),
        νμ€μ°μλΆλ₯λͺ VARCHAR(128),
        ν©μΉλ°μ΄ν° VARCHAR(128),
        FOREIGN KEY(Id) REFERENCES location(Id)
        );""")
  
    # λ°μ΄ν° μ½μ.  
    # μ μ©λ  csv νμΌμ μμΉ μ§μ    
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\property.csv'
  
    with open(csv_file, 'r', encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for id, row in enumerate(reader, start=1):
                cur.execute("""INSERT INTO property(Id, μμ’μ€λΆλ₯λͺ, μμ’μλΆλ₯λͺ, νμ€μ°μλΆλ₯λͺ, ν©μΉλ°μ΄ν°) VALUES (%s, %s, %s, %s, %s);""",
                            (id, row[0],row[1], row[2], row[3]))
            print('making table : property mission completeβ')      
    
        except:
            logging.error("can't insert data")


       
    # 3. νμ΄λΈ μμ± : online - κ°κ² url λ° 'λ€μ΄λ²ν€μλ' λ₯Ό λ΄μ νμ΄λΈ.
    cur.execute("DROP TABLE IF EXISTS online;")
    cur.execute("""CREATE TABLE online(
        Id INTEGER PRIMARY KEY,
        λ€μ΄λ²ν€μλ VARCHAR(128),
        κ°κ²_URL VARCHAR(128),
        FOREIGN KEY(Id) REFERENCES location(Id)
        );""")
  
    # λ°μ΄ν° μ½μ.  
    # μ μ©λ  csv νμΌμ μμΉ μ§μ    
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\online.csv'
    with open(csv_file, 'r',  encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for id, row in enumerate(reader, start=1):
                cur.execute("""INSERT INTO online(Id, λ€μ΄λ²ν€μλ,κ°κ²_URL) VALUES (%s, %s, %s);""",
                            (id, row[0],row[1]))
            print('making table : online mission completeβ')      
    
        except:
            logging.error("can't insert data")   
    


    # 4. νμ΄λΈ μμ± : evaluation - κ°κ² νκ° κ΄λ ¨ λ°μ΄ν°λ₯Ό λ΄μ νμ΄λΈ
    cur.execute("DROP TABLE IF EXISTS evaluation;")
    cur.execute("""CREATE TABLE evaluation(
        Id INTEGER PRIMARY KEY,
        κ°κ²_νμ  FLOAT8,
        νμ μ_μ°Έμ¬ν_μΈμ INTEGER,
        λ°©λ¬Έμ_λ¦¬λ·° VARCHAR(2048),
        λ¦¬λ·°_μ΄μΈμ INTEGER,
        FOREIGN KEY(Id) REFERENCES location(Id)
        );""")
  
    # λ°μ΄ν° μ½μ.  
    # μ μ©λ  csv νμΌμ μμΉ μ§μ    
    csv_file = r'C:\Users\j.park\Section3\real_project3\create_csv\csv_divide\evaluation.csv'
  
    with open(csv_file, 'r',  encoding='utf-8') as f:
        #try:
        reader = csv.reader(f)
        next(reader)
        for id, row in enumerate(reader, start=1):
            cur.execute("""INSERT INTO evaluation(Id, κ°κ²_νμ , νμ μ_μ°Έμ¬ν_μΈμ, λ°©λ¬Έμ_λ¦¬λ·°, λ¦¬λ·°_μ΄μΈμ) VALUES (%s, %s, %s, %s, %s);""",
                        (id, row[0],row[1], row[2], row[3]))


        print('making table : evaluation mission completeβ')      

        #except:
        #    logging.error("can't insert data")   
    

    connection.commit()
    connection.close() 
    
    return None



# --- elephant - sql μ°κ²° μ½λ---

def connect_sql():
    # ele-sql μ°κ²° λ° μλ¬ μ μ΄ 
    # 2κ°μ κ°μ λ¦¬ν΄ν©λλ€.
    
    host = 'castor.db.elephantsql.com'
    user = 'iejeegfa'
    password = 'qjLvYChc-r75m8BZoQFRgNzRWlhNfV4U'
    database = 'iejeegfa'


    try:
        connection = psycopg2.connect(
            host = host,
            user = user,
            database = database,
            password = password)
        cur = connection.cursor()

    except:
        logging.error("could not connect to rds")
    
    return cur, connection