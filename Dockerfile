# 모든 환경 공통 베이스
FROM python:3.9-slim

# 필수 시스템 라이브러리 설치 (AMD64/ARM64 호환 버전)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 설치
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchvision ultralytics -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 복사
COPY ./vision_project /app

# 실행 포트 설정
EXPOSE 8000
CMD ["uvicorn", "vision_project.main:app", "--host", "0.0.0.0", "--port", "8000"]
