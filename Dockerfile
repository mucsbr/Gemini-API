FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml ./
COPY src/ ./src/

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# 设置环境变量
ENV GEMINI_COOKIE_PATH=/data/gemini_webapi \
    PYTHONUNBUFFERED=1

# 创建数据目录
RUN mkdir -p /data/gemini_webapi

# 暴露端口（如果需要）
# EXPOSE 8000

CMD ["python", "-c", "import gemini_webapi; print('Gemini WebAPI installed successfully')"]