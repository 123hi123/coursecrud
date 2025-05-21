FROM python:3.9-slim

WORKDIR /app

# 設置環境變量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製項目文件
COPY . .

# 設置啟動腳本
RUN chmod +x /app/entrypoint.sh

# 創建並切換到非root用戶
RUN mkdir -p /app/data && \
    chmod -R 755 /app && \
    addgroup --system app && \
    adduser --system --group app && \
    chown -R app:app /app

USER app

# 暴露端口
EXPOSE 8000

# 啟動應用
ENTRYPOINT ["/app/entrypoint.sh"] 