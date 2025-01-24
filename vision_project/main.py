from fastapi import FastAPI
from routers.vision_router import router as vision_router
from routers.chatgpt_router import router as chatgpt_router
from routers.ocr_router import router as ocr_router

app = FastAPI(title="Machine Vision & ChatGPT API")

# 라우터 등록 (prefix와 tags로 엔드포인트 구분)
app.include_router(vision_router, prefix="/api/vision", tags=["vision"])
app.include_router(ocr_router, prefix="/api/ocr", tags=["ocr"])
app.include_router(chatgpt_router, prefix="/api/chatgpt", tags=["chatgpt"])

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}