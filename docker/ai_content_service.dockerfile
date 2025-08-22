# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Poetry
RUN pip install poetry

# 先複製 Poetry 設定檔與必要 package 目錄（如 app/ 與 README.md）
COPY pyproject.toml ./
COPY README.md ./
COPY app ./app

# 安裝依賴
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
# 不知道為什麼 poetry 無法透過 pyproject.toml 安裝 google-genai
# 直接在這裡安裝 google-genai
RUN poetry add google-genai==1.28.0

# 再複製其餘專案檔案（如 .env, setup.sh 等）
COPY . .
