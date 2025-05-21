# 學生選課管理系統API

這是一個使用FastAPI框架開發的學生選課管理系統API，提供學生、課程管理和選課功能。

## 功能

- 學生管理：創建、查詢、更新和刪除學生信息
- 課程管理：創建、查詢、更新和刪除課程信息
- 選課管理：學生選課、查詢選課記錄、取消選課

## 技術棧

- Python 3.9+
- FastAPI - Web框架
- SQLAlchemy - ORM
- SQLite - 數據庫
- Docker - 容器化
- GitHub Actions - CI/CD

## 項目結構

```
coursecrud/
├── app/                    # 應用程序代碼
│   ├── api/                # API路由
│   │   ├── endpoints/      # API端點
│   │   │   ├── students.py  # 學生管理API
│   │   │   ├── courses.py   # 課程管理API
│   │   │   └── enrollments.py # 選課管理API
│   │   └── api.py          # API路由集合
│   ├── core/               # 核心配置
│   │   └── config.py       # 配置文件
│   ├── db/                 # 數據庫相關
│   │   ├── database.py     # 數據庫連接
│   │   └── init_db.py      # 數據庫初始化
│   ├── models/             # 數據模型
│   │   └── models.py       # SQLAlchemy模型
│   ├── schemas/            # 數據驗證模式
│   │   ├── student.py      # 學生模式
│   │   ├── course.py       # 課程模式
│   │   └── enrollment.py   # 選課模式
│   ├── tests/              # 測試
│   │   └── test_api.py     # API測試
│   └── main.py             # 應用程序入口
├── .github/                # GitHub Actions配置
│   └── workflows/
│       └── ci.yml          # CI/CD配置
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── requirements.txt        # 依賴項
└── README.md               # 項目說明
```

## 開始使用

### 本地開發

1. 安裝依賴

```bash
pip install -r requirements.txt
```

2. 運行應用

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 使用Docker

1. 使用Docker Compose啟動

```bash
docker-compose up -d
```

2. 訪問API

API將在以下地址運行：

- API文檔: http://localhost:8000/docs
- 健康檢查: http://localhost:8000/

## API文檔

啟動應用後，訪問 http://localhost:8000/docs 查看完整的API文檔。

### 主要端點

- `/api/v1/students/` - 學生管理
- `/api/v1/courses/` - 課程管理
- `/api/v1/enrollments/` - 選課管理

## 測試

運行測試：

```bash
pytest
```

## 部署

項目已配置GitHub Actions CI/CD，推送到main分支後會自動構建Docker鏡像並推送到Docker Hub。

## 開發文檔

### 開發時間記錄

- 專案設計與準備：3小時
  - 需求分析：1小時
  - 技術選型：1小時
  - 數據庫設計：1小時

- 核心功能開發：7小時
  - 專案結構建立：1小時
  - 學生管理API：1.5小時
  - 課程管理API：1.5小時
  - 選課管理API：2小時
  - 功能整合與調試：1小時

- 測試與文檔：2小時
  - 單元測試：1小時
  - API文檔：1小時

- 容器化與部署：3小時
  - Docker配置：1小時
  - CI/CD配置：1小時
  - 部署配置：1小時

- 最終整理：1小時
  - 代碼優化：0.5小時
  - 文檔完善：0.5小時 