from fastapi import FastAPI
from .routers.yolo_router import router as yolo_router
from .routers.chatgpt_router import router as chatgpt_router
from .routers.ocr_router import router as ocr_router
from .routers.product_name_router import router as product_name_router  # 추가

app = FastAPI()

#test
# 라우터 등록 (prefix와 tags로 엔드포인트 구분)
app.include_router(yolo_router, prefix="/api/image/ingredients", tags=["viingredientssion"])
app.include_router(ocr_router, prefix="/api/image/receipt", tags=["receipt"])
app.include_router(chatgpt_router, prefix="/api/chatgpt", tags=["chatgpt"])
app.include_router(product_name_router, prefix="/api/product-names", tags=["product-names"])

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}
