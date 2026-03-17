import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-prod')

    # DB teardown 등록
    from LMS.common.db import init_app
    init_app(app)

    # Blueprint 등록
    from views.main import main_bp
    from views.auth import auth_bp
    from views.board import board_bp
    from views.post import post_bp
    from views.ai import ai_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(board_bp, url_prefix='/board')
    app.register_blueprint(post_bp, url_prefix='/filesboard')
    app.register_blueprint(ai_bp, url_prefix='/ai')

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_APP_PORT', 5000)),
        debug=bool(os.getenv('FLASK_DEBUG', 1)),
    )
