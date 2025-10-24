# app/services/item.py
from typing import List, Optional

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.logger import get_logger

logger = get_logger(__name__)


class ItemService:
    """Item业务逻辑服务类。"""
    
    def get_item(self, db: Session, item_id: int) -> Optional[schemas.Item]:
        """获取单个Item。
        
        Args:
            db: 数据库会话
            item_id: Item ID
            
        Returns:
            Item数据或None
        """
        logger.info(f"Getting item with id: {item_id}")
        item = crud.item.get(db, id=item_id)
        return item
    
    def get_items(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[schemas.Item]:
        """获取Item列表。
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数限制
            
        Returns:
            Item列表
        """
        logger.info(f"Getting items with skip={skip}, limit={limit}")
        items = crud.item.get_multi(db, skip=skip, limit=limit)
        return items
    
    def create_item(
        self, db: Session, item_in: schemas.ItemCreate
    ) -> schemas.Item:
        """创建Item。
        
        Args:
            db: 数据库会话
            item_in: 创建Item的数据
            
        Returns:
            创建的Item数据
        """
        logger.info(f"Creating item: {item_in.name}")
        
        # 这里可以添加业务逻辑验证
        # 例如：检查名称是否重复、价格是否合理等
        
        item = crud.item.create(db, obj_in=item_in)
        logger.info(f"Item created with id: {item.id}")
        return item
    
    def update_item(
        self, db: Session, item_id: int, item_in: schemas.ItemUpdate
    ) -> Optional[schemas.Item]:
        """更新Item。
        
        Args:
            db: 数据库会话
            item_id: Item ID
            item_in: 更新数据
            
        Returns:
            更新后的Item数据或None
        """
        logger.info(f"Updating item with id: {item_id}")
        
        item = crud.item.get(db, id=item_id)
        if not item:
            logger.warning(f"Item with id {item_id} not found")
            return None
        
        item = crud.item.update(db, db_obj=item, obj_in=item_in)
        logger.info(f"Item with id {item_id} updated")
        return item
    
    def delete_item(self, db: Session, item_id: int) -> bool:
        """删除Item。
        
        Args:
            db: 数据库会话
            item_id: Item ID
            
        Returns:
            是否删除成功
        """
        logger.info(f"Deleting item with id: {item_id}")
        
        item = crud.item.remove(db, id=item_id)
        if item:
            logger.info(f"Item with id {item_id} deleted")
            return True
        else:
            logger.warning(f"Item with id {item_id} not found")
            return False


item_service = ItemService()