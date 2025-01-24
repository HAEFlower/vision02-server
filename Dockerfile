# FROM python:3.9
# WORKDIR /app

# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# COPY ./vision_project/ /app

# CMD ["uvicorn", "vision_project.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.9

WORKDIR /app

# 요구 사항 파일 복사
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY ./vision_project/ /app

# uvicorn 실행 후 컨테이너가 종료되지 않도록 tail 명령어로 대기
# sh -c 를 사용해 두 개의 명령어를 한 줄에서 실행
CMD ["sh", "-c", "uvicorn vision_project.main:app --host 0.0.0.0 --port 8000 & tail -f /dev/null"]