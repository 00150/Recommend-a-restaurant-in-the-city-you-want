# https://innate-clove-c5b.notion.site/Cosine-Similarity-664f643b74a54a338065b7a3869576ab(내 노션 -> 코사인 유사도 정리)



#------------------------------------------🔰🔰🔰🔰🔰 코사인 유사도 이용하기. 🔰🔰🔰🔰🔰------------------------------------------------
# 파일 Data_collection.py을 보면 데이터를 모으는 과정에서 하나의 컬럼을 생성하여 데이터를 몰아넣었습니다.
# 우리가 원하는 지역만을 맵핑하여 만든 데이터의 컬럼들중, '중분류명'과 '소분류명'은 활용가치가 큰 데이터입니다.
# 이 데이터들을 Cartegory 데이터라고 지칭하겠습니다.


#❗ 위에서 언급한 카테고리 데이터들의 모습은 다음과 같습니다.
#->양식            정통양식/경양식  
#->커피점/카페     커피전문점/카페/다방
#->한식           한식/백반/한정식


#❗이런 키워드를 담은 데이터들을 하나의 컬럼에 몰아두면 유사도를 계산할 수 있습니다.
#->양식            정통양식/경양식          ------------> 양식 전통양식 경양식
#->커피점/카페     커피전문점/카페/다방      ------------> 커피점 카페 커피전문점 카페 다방
#->한식           한식/백반/한정식           ------------> 한식 한식 백반 한정식


#❗ df['합친데이터'] 라는 컬럼을 생성하여 여기에 
# select_df['업종중분류명'] + select_df['업종소분류명'] +select_df['표준산업분류명'] 의 값을 넣어놨습니다.


# 정리된 데이터를 가져와 코사인 유사도를 실행하여 봅시다.
import re
import pandas as pd
import numpy as np

# 데이터 불러오기
url = r'C:\Users\j.park\Section3\real_project3\create_csv\cleaned_Data.csv'
df = pd.read_csv(url, encoding='utf-8')




# 6월 27일 : 유사도를 이용한 추천 시스템 만들기.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# column : '합친데이터' 에 대하여 TF-IDF를 구한 이후 행렬의 크기 출력.

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['합친데이터'])
print('tf-idf 행렬의 크기(shape):', tfidf_matrix.shape) # tf-idf 행렬의 크기(shape): (278, 83)


# 🤔 what is means that 'tf-idf shape'
# 1. 278개의 가게를 표현하기 위해서 총 83개의 단어를 사용했음을 의미한다.
# 2. 또는 83차원의 문서 벡터가 278개 존재한다고도 표현할 수 있다.


# 🤗 278개의 문서 벡터에 대해서 상호 간의 코사인 유사도를 구하기.
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print('코사인 유사도 결과 :', cosine_sim.shape)  # 코사인 유사도 결과 : (278, 278)


# ❗결과❗
# 1. 코사인 유사도 연산 결과로는 278행, 278열의 행렬을 얻습니다.
# 2. 이는 278개의 각 문서 벡터(가게의 업종 분류명을 모두 합친 컬럼)와 자기 자신을 포함한 278개의 문서 벡터간의 유사도가 기록된 행렬이다.
# 3. 278개의 분류명의 상호 유사도가 모두 기록되어져 있다.



# 🤨 기존 데이터프레임으로부터 '상호명' : 'key', '가게의 인덱스' : 'value' 로 하는 딕셔너리 생성
# dict => title_to_index

title_to_index = dict(zip(df['상호명'], df.index))

# 가게 이름 'Bhc치킨' 의 인덱스 리턴 
idx = title_to_index['Bhc치킨'] #  print(idx)는 36의 값을 지닌다.


# 선택한 영화의 제목을 입력하면 코사인 유사도를 통해 🔱가게의 업종 분류명을 모두 합친 컬럼 : 합친데이터🔱
# 와 가장 유사한 10개의 영화를 찾아내는 함수를 만들어보자.

def get_recommendations(title, cosine_sim=cosine_sim):
    
    # 선택한 영화의 타이틀로부터  해당 영화의 인덱스를 받아오기.
    idx = title_to_index[title]
    
    # 해당 영화와 모든 영화와의 유사도를 가져오기.
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도에 따라 영화들을 정렬한다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 영화를 받아온다.
    sim_scores =sim_scores[1:11]
    
    # 가장 유사한 10개의 영화의 인덱스 가져오기
    movie_indices = [idx[0] for idx in sim_scores]
    
    # 가장 유사한 10개의 영화 제목을 리턴한다.
    return df['상호명'].iloc[movie_indices]

breakpoint()





#--- ❗ 감정분석 기법
#--- 우리가 가져온 리뷰데이터를 이용하여 리뷰의 텍스트가 긍정인지 부정인지 분류하는 것을 의미한다.





#------- 6월 27일 전 생성 코드는 아래와 같다.



# #3. 총 3개의 값이 합쳐진 컬럼 : ['합친데이터'] 을 이용하여 '피처 벡터화'하고 코사인 유사도를 계산하는 코드를 작성합니다. / 사이킷런.

# from sklearn.feature_extraction.text import CountVectorizer  # 피체 벡터화
# from sklearn.metrics.pairwise import cosine_similarity # 코사인 유사도

# #🔆CountVectorizer 
# # 1. 문서를 토큰 리스트로 변환한다.
# # 2. 각 문서에서 토큰의 출현 빈도를 센다.
# # 3. 각 문서를 BOW 인코딩 벡터로 변환한다.

# count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2))

# # min_df : 단어장에 포함되기 위한 최소 빈도 (※ 기본값 : 1)
# # ngram_range:  n-그램 범위로 단어를 몇 개로 토큰화 할지를 의미합니다.






# place_category = count_vect_category.fit_transform(df['합친데이터']) 
# place_simi_cate = cosine_similarity(place_category, place_category) 
# place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]


# applied_cosine_category = cosine_similarity(place_category, place_category)
# place_simi_cate_sorted_ind = applied_cosine_category.argsort()[:, ::-1]

# # 이렇게 하면, 각각의 데이터 vs 데이터들이 서로 카테고리 텍스트가 얼마나 유사한지를 따져줍니다.
# # 500개의 데이터가 있다면 1번은 자기 자신과 한 번 비교하고, 나머지 499개와 비교를 하게 됩니다.
# # 이 데이터를 바탕으로 마지막 단계에서 최종 채점 단계에서 활용합니다.




# # df['합친데이터']를 이용하여 코사인 유사도를 계산했던 것처럼 리뷰 텍스트 컬럼을 이용하여 같은 작업을 진행하여 줍니다.

# # 리뷰 텍스트 컬럼 간의 텍스트 피쳐를 벡터라이징합니다.
# count_vect_review = CountVectorizer(min_df=2, ngram_range = (1,2))
# place_review = count_vect_review.fit_transform(df['방문자_리뷰'])

# # 리뷰 텍스트 간의 코사인 유사도를 따져줍니다.
# place_simi_review = cosine_similarity(place_review, place_review)
# place_simi_review_sorted_ind = place_simi_review.argsort()[:,::-1]



# # 이후 다양한 요소를 종합하는 식을 계산하여 알고리즘에 적용하여 줍니다.
# """
# 공식 1: 카테고리가 얼마나 유사한지
# 공식 2: 텍스트 리뷰가 얼마나 유사한가
# 공식 3: 텍스트 리뷰가 올라온 개수
# 공식 4: 가게 평점
# 공식 5: 가게 별점 평가에 얼마나 많은 인원이 참여하였는지 
# """
#  # '컬럼 : 합친 데이터' 에 대한 카테고리 유사도
#  # '컬럼 : 방문자_리뷰'에 대한 카테고리 유사도
#  # 방문자 리뷰가 달린 총 개수
 
# applied_formula = (place_simi_cate* 0.3
#                    + place_simi_review * 1 
#                    + np.repeat([df['리뷰_총인원'].values], len(df['리뷰_총인원']), axis=0) * 0.001 
#                    + np.repeat([df['가게_평점'].values], len(df['가게_평점']), axis=0) *0.005
#                    + np.repeat([df['평점에_참여한_인원'].values], len('평점에_참여한_인원'), axis=0) * 0.001)


# place_simi_co_sorted_ind = applied_formula.argsort()[:,::-1]

# #함수 구현
# def find_place(df,sorted_ind, place_name, top_n=10):
#     place_title = df[df['상호명'] == place_name]
#     place_index = place_title.index.values
#     similar_indexes = sorted_ind[place_index, :(top_n)]
#     similar_indexes = similar_indexes.reshape(-1)
#     return df.iloc[similar_indexes]


# breakpoint()


# # ❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗문제점 발견❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗
# # 코사인 유사도 적용시, 적용되는 데이터 컬럼에 np.nan의 값이 존재하면 안된다.
# #df['방문자_리뷰']에 적용하는 도중  
# # ValueError: np.nan is an invalid document, expected byte or unicode string. 의 오류가 떠서 값이 없는 부분은 '없음'으로 대체한다.
# # data_cleaning에 적용하도록 하자.