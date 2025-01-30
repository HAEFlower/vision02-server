import torch
import numpy as np
import cv2
import pytesseract
import pickle  # For saving the object state
from PIL import Image


def process_prescription(image):
    if image is None:
        return "이미지를 불러올 수 없습니다."

    # 이미지 크기 조정
    image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    # 이미지 전처리
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # 대비 향상
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(blur)

    # 모폴로지 연산
    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.morphologyEx(enhanced, cv2.MORPH_CLOSE, kernel)

    # 노이즈 제거 및 선명도 향상
    denoised = cv2.fastNlMeansDenoising(processed)
    sharpened = cv2.GaussianBlur(denoised, (0, 0), 3)
    sharpened = cv2.addWeighted(denoised, 1.5, sharpened, -0.5, 0)

    # 오츠의 이진화
    thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # OCR 수행
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(thresh, lang="kor+eng", config=custom_config)

    # 결과 이미지에 표시
    result_image = image.copy()

    return {"text": text, "processed_image": result_image}


def run_inference(image: Image.Image):
    img = np.array(image)
    return process_prescription(img)
