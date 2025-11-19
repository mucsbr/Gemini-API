FROM python:3.11-slim

WORKDIR /app

COPY app.py ./

RUN pip install --no-cache-dir -U gemini-webapi fastapi uvicorn && \
    mkdir -p /data/gemini_webapi

ENV GEMINI_COOKIE_PATH=/data/gemini_webapi \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]