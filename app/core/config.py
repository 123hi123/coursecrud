import os
from pathlib import Path

# 項目根目錄
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 數據庫設置
SQLITE_DB_URL = f"sqlite:///{BASE_DIR}/sql_app.db"
DATABASE_URL = os.getenv("DATABASE_URL", SQLITE_DB_URL)

# API設置
API_V1_STR = "/api/v1"
PROJECT_NAME = "學生選課管理系統"

# 安全設置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # 在生產環境中應更改
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 