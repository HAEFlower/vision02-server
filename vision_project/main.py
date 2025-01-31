from fastapi import FastAPI
from .routers.yolo_router import router as yolo_router
from .routers.chatgpt_router import router as chatgpt_router
from .routers.ocr_router import router as ocr_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTPS 강제 리다이렉트 미들웨어
app.add_middleware(HTTPSRedirectMiddleware)

# 프록시 헤더 신뢰 설정
app = FastAPI(
    servers=[{"url": "https://magnetic-oriented-poodle.ngrok-free.app"}],
)

# 라우터 등록 (prefix와 tags로 엔드포인트 구분)
app.include_router(yolo_router, prefix="/api/image/ingredients", tags=["ingredients"])
app.include_router(ocr_router, prefix="/api/image/receipt", tags=["receipt"])
app.include_router(chatgpt_router, prefix="/api/chatgpt", tags=["chatgpt"])


@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}
