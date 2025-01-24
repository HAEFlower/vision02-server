from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
from vision_project.vision_model.yolo_model import load_model, run_inference

router = APIRouter()

# 앱 시작 시 1회 모델 로딩 (데모용)
vision_model = load_model()

@router.post("/")
async def vision_inference(file: UploadFile = File(...)):
    """
    머신 비전 추론 엔드포인트.
    이미지 파일을 받아서 모델 추론 후 결과를 반환.
    """
    try:
        # 이미지 파일을 PIL Image로 변환
        contents = await file.read()
        image = Image.open(bytes(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 처리 오류: {str(e)}")

    # 추론 실행
    result = run_inference(vision_model, image)

    # 추론 결과 분석

    # gpt-3.5-turbo 엔진을 사용해 이미지에 대한 설명 생성

    # 추론 결과 반환
    return {"data": result}