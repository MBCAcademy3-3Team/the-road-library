import cv2
import torch
import base64
import time
from ultralytics import YOLO


class WebCamService:
    _model = None
    _target_label = ""
    _device = 'cuda' if torch.cuda.is_available() else 'cpu'
    _running = False

    @classmethod
    def load_model(cls):
        if cls._model is None:
            cls._model = YOLO('yolov8n.pt')
            cls._model.to(cls._device)
            print(f"[WebCam] 모델 로드 완료 (Device: {cls._device})", flush=True)
        return cls._model

    @classmethod
    def set_target(cls, label: str):
        cls._target_label = label.strip().lower()

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def run_webcam_stream(cls, socketio, cam_index=0):
        print(f"[WebCam] 스트리밍 시작 (cam_index: {cam_index})", flush=True)
        cls._running = True

        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print(f"[WebCam ERROR] 웹캠 연결 실패", flush=True)
            socketio.emit('webcam_error', {'message': '웹캠 연결 실패'})
            return

        model = cls.load_model()
        frame_count = 0

        while cap.isOpened() and cls._running:
            ret, frame = cap.read()
            if not ret:
                socketio.sleep(0.1)
                continue

            frame = cv2.resize(frame, (640, 480))
            frame_count += 1

            if frame_count % 3 != 0:
                continue

            results = model.predict(frame, device=cls._device, conf=0.7, verbose=False, imgsz=640)
            boxes = results[0].boxes
            annotated_frame = results[0].plot()

            _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            encoded_image = base64.b64encode(buffer).decode('utf-8')

            socketio.emit('webcam_frame', {
                'image': encoded_image,
                'count': frame_count
            })

            if cls._target_label and boxes is not None:
                detected_names = [model.names[int(i)].lower() for i in boxes.cls.tolist()]
                if cls._target_label in detected_names:
                    socketio.emit('webcam_alert', {
                        'label': cls._target_label,
                        'time': time.strftime('%H:%M:%S')
                    })

            socketio.sleep(0.01)

        cap.release()
        cls._running = False
        print(f"[WebCam] 스트리밍 종료", flush=True)