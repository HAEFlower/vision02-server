from fastapi import APIRouter, HTTPException, Body
from ..domain.openai.request_gpt import ask_chatgpt, get_image

router = APIRouter()

@router.post("/")
async def chatgpt_query(
    ingredients: list[str] = Body(...),
    cookingGoal: str = Body(...),
    cookingMethod: str = Body(...),
    ):
    """
    ChatGPT 엔드포인트.
    사용자의 프롬프트를 받아 GPT 모델에 질의 후 결과 반환.
    """
    try:
        answer = ask_chatgpt(ingredients, cookingGoal, cookingMethod)
        return answer
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"오류: {str(ex)}")


@router.get("/image")
async def chatgpt_query(
    name: str = Body(..., embed=True)
    ):
    """
    ChatGPT 엔드포인트.
    사용자의 프롬프트를 받아 GPT 모델에 질의 후 결과 반환.
    """
    try:
        answer = get_image(name)
        return answer
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"오류: {str(ex)}")
