# 블루 프린트 사용
# 🚀Why use Blueprint in making apps?
# 홈페이지 기능이 많아질수록 라우트가 많아집니다.
# 그렇기 때문에 이러한 라우트를 하나의 파일로 모아서 사용하지 않고, 기능별로 나눠 블루프린트 기능을 사용합니다.
# 블루프린트는 FLASK에서 여러 개의 라우트를 한 곳에 묶어둘 수 있는 기능이 존재합니다.
import sqlite3
import psycopg2
import logging




# elephant 연결 : 패키지 불러오기. (생성한 함수를 사용하기 위한 패키지 불러오가)
from selfmade_function import Handmade_function as hf


    




#모듈 import
from flask import Blueprint, render_template


#------범박동 관련------
bp = Blueprint('범박동', __name__, url_prefix='/범박동', template_folder = 'sample')

@bp.route('/')
def index():
    



    return render_template('범박동.html')



#------괴안동 관련------
bp1 = Blueprint('괴안동', __name__, url_prefix='/괴안동', template_folder = 'sample')

@bp1.route('/')
def index():    


    return render_template('괴안동.html')



#------소사동 관련------
bp2 = Blueprint('소사동', __name__, url_prefix='/소사동', template_folder = 'sample')

@bp2.route('/')
def index():    


    return render_template('소사동.html')



#------소사본동 관련------
bp3 = Blueprint('소사본동', __name__, url_prefix='/소사본동', template_folder = 'sample')

@bp3.route('/')
def index():    


    return render_template('소사본동.html')

