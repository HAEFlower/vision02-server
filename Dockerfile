# 사용할 베이스 이미지 설정 (Python 3.9)
FROM python:3.9

# 컨테이너 내 작업 디렉터리 생성 및 이동
WORKDIR /app

# 요구 사항 파일 복사
COPY requirements.txt /app/

# 라이브러리 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY ./vision_project/ /app

# FastAPI 애플리케이션 실행
# main.py 파일에서 uvicorn.run(app, host="0.0.0.0", port=8000) 형태로 
# 실행되도록 코드를 작성했을 경우 해당 CMD가 필요 없음
CMD ["uvicorn", "vision_project.main:app", "--host", "0.0.0.0", "--port", "8000"]