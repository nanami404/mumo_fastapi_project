# app/models/item.py
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.session import Base


class Item(Base):
    """Item数据库模型。"""
    
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True, comment="物品ID")
    name = Column(String(100), nullable=False, index=True, comment="物品名称")
    description = Column(String(500), nullable=True, comment="物品描述")
    price = Column(Float, nullable=False, comment="物品价格")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")