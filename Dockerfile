From python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements 설치
COPY requirements.txt .
RUN pip install --upgrade pip & pip install -r requirements.txt

# 앱 코드 복사
COPY . .

# 실행 권한 부여
RUN chmod +x /app/init.sh

# 실행 명령어
CMD ["sh", "/app/init.sh"]
