# 블루 프린트 사용
# 🚀Why use Blueprint in making apps?
# 홈페이지 기능이 많아질수록 라우트가 많아집니다.
# 그렇기 때문에 이러한 라우트를 하나의 파일로 모아서 사용하지 않고, 기능별로 나눠 블루프린트 기능을 사용합니다.
# 블루프린트는 FLASK에서 여러 개의 라우트를 한 곳에 묶어둘 수 있는 기능이 존재합니다.

#모듈 import
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def index():
    return 'Here is blueprint'