# 1. 사용할 파이썬 공식 이미지를 기반으로 설정합니다. (최신 버전 사용)
FROM python:3.11-slim

# 2. 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 3. 파이썬 환경 변수 설정 (로그 즉시 출력, .pyc 파일 미생성)
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# 4. requirements.txt를 먼저 복사하여 종속성을 설치합니다. (빌드 캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 보안을 위해 non-root 사용자를 생성하고 해당 사용자로 전환합니다.
RUN addgroup --system app && adduser --system --group app

# 6. 나머지 애플리케이션 코드를 복사합니다.
COPY . .

# 7. 코드 파일들의 소유권을 새로 생성한 app 사용자로 변경합니다.
RUN chown -R app:app /app

# 8. 컨테이너 실행 사용자를 app으로 설정합니다.
USER app

# 9. 컨테이너가 5000번 포트를 사용함을 알립니다.
EXPOSE 5000

# 10. 컨테이너 시작 시 Gunicorn으로 Flask 앱을 실행합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]