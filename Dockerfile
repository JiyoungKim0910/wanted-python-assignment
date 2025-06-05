From python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements 설치
COPY requirements.txt .
RUN pip install --upgrade pip & pip install -r requirements.txt

# 앱 코드 복사
COPY . .

# 컨테이너 실행 시 명령어
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]