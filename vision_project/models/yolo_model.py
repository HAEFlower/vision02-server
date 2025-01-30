from PIL import Image
from ultralytics import YOLO


def load_model():
    model = YOLO("./vision_project/models/yolo/best.pt", verbose=False)
    model.fuse()  # 모델 최적화
    return model


def run_inference(model, image: Image.Image):
    """
    모델에 이미지를 입력해 추론을 실행하는 함수.
    """
    # 이미지 전처리

    # 모델 추론 실행
    # result = model(image)
    result = model.predict(image)

    return result
