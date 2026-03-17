from flask import Blueprint, render_template, request, jsonify, session

from LMS.common.session import Session
from LMS.service.AIService import AIService

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/')
def index():
    return render_template('ai/index.html')


@ai_bp.route('/ask', methods=['POST'])
def ask():
    """AI에게 질문 (JSON API)"""
    data = request.get_json()
    if not data or not data.get('question'):
        return jsonify({'error': '질문을 입력해주세요.'}), 400

    question = data['question'].strip()
    history = data.get('history', [])

    try:
        answer = AIService.ask(question, history)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': f'AI 응답 중 오류가 발생했습니다: {str(e)}'}), 500
