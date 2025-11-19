FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

ENV GEMINI_COOKIE_PATH=/data/gemini_webapi

CMD ["python"]