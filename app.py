from dotenv import load_dotenv
load_dotenv()

# 기본 모듈
import os

# 라이브러리
from flask import Flask, render_template, g
from flask import Flask
from flask_caching import Cache

# 서비스 모듈
from LMS.service.MemberService import member_bp

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')

# Cache 설정
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# 메인 페이지 라우트
@app.route('/')
def index():
    return render_template('main.html')

# Blueprint 등록
# TODO : app.py에 등록할 때 항상 url_prefix를 붙여서 넣기
app.register_blueprint(member_bp, url_prefix='/member')

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 서버 실행부
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_APP_PORT', 5000)),
        debug=bool(os.getenv('FLASK_DEBUG', 1)),
    )