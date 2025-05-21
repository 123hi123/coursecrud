#!/bin/bash
set -e

# 確保 data 目錄存在
mkdir -p /app/data

# 輸出一些調試信息
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Files in current directory:"
ls -la

# 初始化數據庫
python -c "from app.db.init_db import init_db; init_db()"

# 啟動應用
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 "$@" 