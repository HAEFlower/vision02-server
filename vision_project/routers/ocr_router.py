import io
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from PIL import Image
from ..models.ocr_model import load_model, run_inference
from ..utils.dummy import get_response_dummy

router = APIRouter()

# 앱 시작 시 1회 모델 로딩 (데모용)
ocr_model = load_model()


@router.post("/")
async def ocr_inference(
    file: UploadFile = File(...),
    cookingGoal: str = Form(...),
    cookingMethod: str = Form(...),
):
    """
    머신 비전 추론 엔드포인트.
    이미지 파일을 받아서 모델 추론 후 결과를 반환.
    """
    try:
        # 업로드 파일을 비동기로 읽어 바이트 배열 획득
        contents = await file.read()

        # io.BytesIO로 래핑해 PIL에서 열 수 있는 파일 객체 형태로 만들기
        image = Image.open(io.BytesIO(contents))
        # RGB 변환 (원본이 PNG, JPEG 등일 경우에도 일관성 있게 RGB 처리)
        image = image.convert("RGB")

    except Exception as e:
        # 이미지 파일이 손상되어 있거나, Pillow가 처리할 수 없는 형식일 경우 예외 발생
        raise HTTPException(status_code=400, detail=f"이미지 처리 오류: {str(e)}")

    # 추론 실행
    # result = run_inference(ocr_model, image)

    # 추론 결과 분석

    # gpt-3.5-turbo 엔진을 사용해 이미지에 대한 설명 생성

    # 추론 결과 반환
    return get_response_dummy()
