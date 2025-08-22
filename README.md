<!-- @format -->

# ai_content_service

## 專案簡介

本專案為 AI 內容引擎（Python + FastAPI），採用微服務架構，負責關鍵字蒐集、AI 文章生成等重型任務，並與主系統（Laravel）透過 RESTful API 溝通。

---

## 技術堆疊

- Python 3.10+
- FastAPI
- Uvicorn
- Poetry（依賴管理）
- Docker / Docker Compose
- Black、Ruff、Mypy（程式碼品質工具）

---

## 快速開始

### 1. 前置需求

- 已安裝 [Git](https://git-scm.com/)
- 已安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 2. 一鍵初始化

```bash
# 1. 複製專案
git clone <your-repo-url>
cd ai_content_service

# 2. 執行初始化腳本（自動產生 .env 並安裝依賴）
sh setup.sh

# 3. 啟動服務
# 使用 Docker Compose 啟動所有服務
#（會自動讀取 .env 設定）
docker-compose up --build
```

### 3. 驗證環境

啟動成功後，瀏覽器開啟 http://localhost:8000/docs
若能看到 FastAPI 自動產生的 API 文件頁面，代表環境建置成功。

---

## 目錄結構

```
ai_content_service/
├── app/                # 主程式碼
├── tests/              # 測試
├── .env.example        # 環境變數範本
├── setup.sh            # 一鍵初始化腳本
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml      # Poetry 設定
├── README.md
```

---

## 其他說明

- 請勿將 `.env` 檔案提交至版本控制。
- 若有任何問題，請參考 PRD 文件或聯絡專案負責人。
