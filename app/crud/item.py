# app/crud/item.py
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem:
    """Item CRUD操作类。"""
    
    def get(self, db: Session, id: int) -> Optional[Item]:
        """根据ID获取Item。
        
        Args:
            db: 数据库会话
            id: Item ID
            
        Returns:
            Item实例或None
        """
        return db.query(Item).filter(Item.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """获取多个Item。
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数限制
            
        Returns:
            Item列表
        """
        return db.query(Item).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: ItemCreate) -> Item:
        """创建Item。
        
        Args:
            db: 数据库会话
            obj_in: 创建Item的数据
            
        Returns:
            创建的Item实例
        """
        db_obj = Item(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: Item, obj_in: ItemUpdate
    ) -> Item:
        """更新Item。
        
        Args:
            db: 数据库会话
            db_obj: 要更新的Item实例
            obj_in: 更新数据
            
        Returns:
            更新后的Item实例
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Optional[Item]:
        """删除Item。
        
        Args:
            db: 数据库会话
            id: Item ID
            
        Returns:
            删除的Item实例或None
        """
        obj = db.query(Item).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


item = CRUDItem()