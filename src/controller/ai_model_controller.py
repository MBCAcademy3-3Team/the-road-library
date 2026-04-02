# src/controller/ai_model_controller.py
from flask import Blueprint, request, session, render_template, jsonify, Response
from src.common import login_required
from src.service.ai_model_service import AIModelService

model_bp = Blueprint('model', __name__)
ai_model_service = AIModelService()


@model_bp.route('/', methods=['GET'])
@login_required
def get_model_page():
    return render_template('ai_model/model.html')


@model_bp.route('/video_feed/<filename>')
@login_required
def video_feed(filename):
    try:
        stream = ai_model_service.get_video_stream(filename)
        return Response(
            stream,
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except FileNotFoundError as e:
        return str(e), 404


@model_bp.route('/detect', methods=['POST'])
@login_required
def detect_objects():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        result = ai_model_service.detect_image(request.files['file'])
        return jsonify({'success': True, **result})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@model_bp.route('/save_result', methods=['POST'])
@login_required
def save_result():
    user_id = session.get('user_id')
    file    = request.files.get('merged_image')

    if not file or not user_id:
        return jsonify({'success': False, 'message': '로그인 정보 또는 파일이 없습니다.'}), 400

    try:
        boar_count       = int(request.form.get('boar_count', 0))
        water_deer_count = int(request.form.get('water_deer_count', 0))
        racoon_count     = int(request.form.get('racoon_count', 0))
    except (ValueError, TypeError):
        boar_count = water_deer_count = racoon_count = 0

    try:
        result_url = ai_model_service.save_result(
            user_id          = user_id,
            file             = file,
            original_filename= request.form.get('original_filename', ''),
            boar_count       = boar_count,
            water_deer_count = water_deer_count,
            racoon_count     = racoon_count,
        )
        return jsonify({
            'success': True,
            'url':     result_url,
            'message': 'Cloudinary 업로드 및 DB 저장 성공!'
        })
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500