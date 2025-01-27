import io
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from PIL import Image
from ..models.yolo_model import load_model, run_inference
from ..utils.dummy import get_response_dummy
from ..utils.ingredients_list import get_ingredient_by_id, get_ingreidients_list_by_ids
from ..domain.openai.request_gpt import ask_chatgpt

router = APIRouter()

# 앱 시작 시 1회 모델 로딩 (데모용)
yolo_model = load_model()


@router.post("/")
async def vision_inference(
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
        image = Image.open(io.BytesIO(contents)).convert("RGB")

    except Exception as e:
        # 이미지 파일이 손상되어 있거나, Pillow가 처리할 수 없는 형식일 경우 예외 발생
        raise HTTPException(status_code=400, detail=f"이미지 처리 오류: {str(e)}")

    # 추론 실행
    result = run_inference(yolo_model, "./vision_project/models/Unseen_2.png")

    # 추론 결과 분석
    print(f"result: {result}")
    # ingredients = get_ingreidients_list_by_ids(result)
    # gpt api를 사용해 이미지에 대한 설명 생성
    # response = ask_chatgpt(ingredients, cookingGoal, cookingMethod)

    # 추론 결과 반환
    return get_response_dummy()
