import os

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def index():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_APP_PORT', 5000)),
        debug=bool(os.getenv('FLASK_DEBUG', 1)),
    )