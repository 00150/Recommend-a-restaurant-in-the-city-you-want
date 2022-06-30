# #flask 모듈 import
# from flask import Flask

# #생성한 Blueprint 모듈 import
# from play_app.routes import user_routes

# app = Flask(__name__)
# #생성한 Blueprint 모듈 등록
# app.register_blueprint(user_routes.bp)


# # 기본 페이지
# @app.route('/')
# def index():
#     return 'Hi, bro'

# # 연결페이지 1
# @app.route('/index/', defaults= {'num':0})
# @app.route('/index/<num>')
# def index_number(num):
#     return 'Here is "index : main" page'


# if __name__ == '__main__':
#     app.run(debug=True)


#------------------------------🏗 Application Factory -------------------------------
# https://flask-docs-kr.readthedocs.io/ko/latest/patterns/appfactories.html 

# ✅ Flask 의 HTML 렌더링 : render_template import 하기.

from flask import Flask, render_template

# 🐵 참고 : jinja 템플릿 활용
# flask 또한 HTML 파일들을 제공하면서 웹 페이지를 클라이언트에게 보여줄 수 있습니다.
# 우리는 단순히 정해진 변경되지 않는 데이터와 페이지가 아닌 상황에 따라 다른 정보를 웹페이지로 넘겨줘야 합니다.
# flask에서는 render_template 이라는 메소드로 html 파일들을 불러올 수 있는 방법이 있습니다
# 해당 함수는 기본적으로 프로젝트 폴더 내에 'templates' 라는 이름의 폴더를 기본 경로로 설정합니다. 
# 따라서 먼저 templates 폴더를 만들고 내부에 html 파일들을 모아두면 손쉽게 사용할 수 있습니다.


def create_app():
    app = Flask(__name__)
    
    
    #기본 : 메인 페이지 문구
    @app.route('/')
    def index():
        return render_template('main.html')
    
    
    
    #생성한 Blueprint 모듈 import
    from playapp.routes import user_routes
    #생성한 Blueprint 모듈 등록
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(user_routes.bp1)
    app.register_blueprint(user_routes.bp2)
    app.register_blueprint(user_routes.bp3)
    
    return app





if __name__ == "__main__":
    app = create_app()
    app.run()
    