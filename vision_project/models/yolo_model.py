from PIL import Image
from ultralytics import YOLO

def load_model():
    """
    실제 딥러닝 모델을 불러오는 로직.
    여기서는 단순히 None 반환으로 예시 처리.
    """
    model = YOLO("./vision_project/models/best.pt")
    return model


def run_inference(model, image: str):
    """
    모델에 이미지를 입력해 추론을 실행하는 함수.
    """

    # 이미지 전처리
    
    # 모델 추론 실행
    
    # 추론 결과를 임시로 "dummy"로 설정
    result = model(image)
    return result
