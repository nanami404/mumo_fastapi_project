# app/schemas/item.py
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Item基础模型。"""
    
    name: str = Field(..., description="物品名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="物品描述", max_length=500)
    price: float = Field(..., description="物品价格", ge=0)
    is_active: bool = Field(True, description="是否激活")


class ItemCreate(ItemBase):
    """创建Item的请求模型。"""
    pass


class ItemUpdate(BaseModel):
    """更新Item的请求模型。"""
    
    name: Optional[str] = Field(None, description="物品名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="物品描述", max_length=500)
    price: Optional[float] = Field(None, description="物品价格", ge=0)
    is_active: Optional[bool] = Field(None, description="是否激活")


class Item(ItemBase):
    """Item响应模型。"""
    
    id: int = Field(..., description="物品ID")
    
    class Config:
        from_attributes = True