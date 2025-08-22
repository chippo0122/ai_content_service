<!-- @format -->

# ai_content_service App 說明

本目錄為 AI 內容引擎（Python FastAPI 專案）的主程式碼區。

## 主要功能

- 關鍵字自動蒐集（Google Trends 等）
- 與外部 AI 服務（如 Google Gemini）串接
- 文章自動生成與審核流程
- 提供 RESTful API 供主系統呼叫
- 支援背景任務與排程（Celery/Celery Beat）

## 目錄結構建議

- `main.py`：FastAPI 入口點
- 其他模組（如 routers、services、schemas、tasks）可依需求擴充

## 注意事項

- 請勿將敏感資訊（如 .env）放入版本控制
- 程式碼請遵循專案的格式化與靜態檢查規範（Black、Ruff、Mypy）
