import logging
from sqlalchemy.orm import Session

from app.db.database import Base, engine
from app.models import models
from app.core.config import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    # 創建所有表
    logger.info(f"正在創建數據庫表，連接至 {DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    logger.info("數據庫表創建完成")

if __name__ == "__main__":
    init_db() 