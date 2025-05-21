from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import API_V1_STR, PROJECT_NAME
from app.db.init_db import init_db

app = FastAPI(
    title=PROJECT_NAME,
    description="提供學生、課程管理和選課功能的後端服務",
    version="0.1.0",
)

# 初始化數據庫（在生產環境中會使用迁移工具）
@app.on_event("startup")
async def startup_event():
    init_db()

# 設定CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中應限制為特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"歡迎使用{PROJECT_NAME} API", "docs_url": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 