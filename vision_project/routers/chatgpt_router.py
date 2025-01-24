from fastapi import APIRouter, HTTPException, Body
from ..domain.openai.request_gpt import ask_chatgpt

router = APIRouter()

@router.post("/")
async def chatgpt_query(prompt: str = Body(..., embed=True)):
    """
    ChatGPT 엔드포인트.
    사용자의 프롬프트를 받아 GPT 모델에 질의 후 결과 반환.
    """
    print(f"ChatGPT 질의: {prompt}")
    try:
        answer = ask_chatgpt(prompt)
        return {"prompt": prompt, "answer": answer}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"오류: {str(ex)}")