from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
import io
import json
from ..domain.openai.extract_product_names import extract_product_names
from ..domain.openai.request_gpt import ask_chatgpt
from ..models.ocr_model import run_inference

router = APIRouter()


@router.post("")
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
    result = run_inference(image)

    # 추론 결과 텍스트를 사용하여 상품명 추출
    receipt_text = result["text"]

    product_names = extract_product_names(receipt_text)

    # GPT 모델을 사용하여 레시피 결과물 추출
    try:
        recipe_result = ask_chatgpt(product_names, cookingGoal, cookingMethod)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT 요청 오류: {str(e)}")

    # 최종 결과 반환
    return recipe_result
