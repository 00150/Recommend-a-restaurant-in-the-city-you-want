#❗감정분석에 사용될  train 샘플 데이터를 만들고 있습니다.❗
# 만들어지는 csv 파일은 create_csv/traindata에 담겨있으니 확인바랍니다.
# Handmade_function.py로 생성된 함수 또한 경로가 위에 언급한 위치로 바뀌었으니, 확인바랍니다.


from selfmade_function import Handmade_function
import pandas as pd
import numpy as np
import csv
import os


#1. 사용할 데이터의 경로 설정 및 데이터 가져오기.
data = os.path.join(os.getcwd(),'경기상권정보.csv')
df = pd.read_csv(data)


#2. 음식에 해당하는 데이터만 출력 및 사용할 컬럼만 지정하기.
df = df.loc[df['상권업종대분류명'] == '음식']

columns =['상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도']
df = df[columns]


#3. 입력하는 동을 기준으로, 원하는 데이터만 출력 및 따로 저장하기. 
#3-1. 찾고자 하는 동의 이름을 입력 받습니다. 
# ❗ 다음과 같은 지역에서 샘플 데이터를 얻어왔습니다.
#  역삼동, 성남동, 망월동, 상대원동, 죽전동

dong = input('찾고자하는 동네의 동 이름을 입력하세요😆 : ').replace(" ", '').split(',') 
select_dong = dong



# # ---> 함수를 생성하여 이용하겠습니다.
def mapping_address():
      #3-1. 찾고자 하는 동의 이름을 입력 받습니다.
  #dong = input('찾고자하는 동네의 동 이름을 입력하세요😆 : ').replace(" ", '').split(',') # 역삼동, 성남동, 망월동, 상대원동, 죽전동
  dong_name = select_dong

  #3-2. 기본 데이터 생성
  default_data = pd.DataFrame(columns = {'상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도'})  

  #3-3. for문을 통해 기입한 동이름으로만 데이터를 따로 구성합니다.
  for number in range(len(dong_name)):
    add_df = df.loc[(df['행정동명'] == dong_name[number])]
    default_data = pd.concat([add_df, default_data])
  
  #3-4.컬럼명 단순화
  # 추려진 데이터를 확인해보면 컬럼명의 어휘가 조금 어렵습니다. 보다 이용에 편리하도록 편리한 컬럼명으로 바꿔줍니다.
  default_data.columns = ['상호명',
                          '업종중분류명',
                          '업종소분류명',
                          '표준산업분류명',
                          '행정동명',
                          '위도',
                          '경도']

  
  #3-5. 원하는 지역으로 구성된 데이터프레임을 따로 저장합니다. 
  default_data.to_csv('c:/Users/j.park/Section3/real_project3/create_csv/traindata/SELECT_REGION.csv', index = False, encoding= 'cp949')
  







#-------- 이후 실행하여 봅시다. 
mapping_address()
