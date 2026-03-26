from flask import Blueprint, render_template, request, jsonify
from src.common import login_required
from ultralytics import YOLO
import os

model_bp = Blueprint('model', __name__)

# 1. YOLOv11 모델 로드
MODEL_PATH = 'static/model/best.pt'
model = YOLO(MODEL_PATH)


@model_bp.route('/', methods=['GET'])
@login_required
def get_model_page():
    return render_template('ai_model/model.html')


@model_bp.route('/detect', methods=['POST'])
@login_required
def detect_objects():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # 2. 임시 파일 저장
    temp_path = os.path.join('static/temp', file.filename)
    os.makedirs('static/temp', exist_ok=True)
    file.save(temp_path)

    try:
        # 3. YOLO 분석 실행 (영상 처리를 위해 stream=True 추가)
        # stream=True는 대용량 영상 분석 시 메모리 부족(OOM)을 방지합니다.
        results = model.predict(temp_path, save=False, stream=True)

        # 모델의 영어 클래스명을 프론트엔드용 한글로 매핑
        label_map = {
            'boar': '멧돼지',
            'water_deer': '고라니',
            'rabbit': '멧토끼',
            'squirrel': '다람쥐',
            'heron': '왜가리'
        }

        # 데이터 초기화
        counts = {"멧돼지": 0, "고라니": 0, "멧토끼": 0, "다람쥐": 0, "왜가리": 0}
        detections = []

        # results가 제너레이터이므로 반복문을 통해 각 프레임의 결과를 가져옵니다.
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                eng_label = model.names[cls_id]
                kor_label = label_map.get(eng_label, eng_label)
                conf = float(box.conf[0])

                if kor_label in counts:
                    counts[kor_label] += 1

                # 영상의 경우 너무 많은 데이터가 쌓일 수 있으므로
                # 신뢰도가 어느 정도 높은 결과만 리스트에 추가합니다.
                if conf > 0.25:
                    detections.append({
                        'label': kor_label,
                        'conf': f"{conf * 100:.1f}%"
                    })

        # 4. 결과 반환
        # 영상 분석 결과가 너무 길면 프론트엔드가 느려지므로 상위 30개 정도만 보냅니다.
        return jsonify({
            'success': True,
            'counts': list(counts.values()),
            'detections': detections[:30]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)