# app/api/deps.py
from typing import Generator

from sqlalchemy.orm import Session

from app.core.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话依赖。
    
    Yields:
        数据库会话实例
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()