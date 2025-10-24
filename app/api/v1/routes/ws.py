# app/api/v1/routes/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


class ConnectionManager:
    """WebSocket连接管理器。"""
    
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """接受WebSocket连接。
        
        Args:
            websocket: WebSocket连接实例
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        """断开WebSocket连接。
        
        Args:
            websocket: WebSocket连接实例
        """
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """发送个人消息。
        
        Args:
            message: 消息内容
            websocket: 目标WebSocket连接
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """广播消息给所有连接。
        
        Args:
            message: 广播消息内容
        """
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> None:
    """WebSocket端点。
    
    Args:
        websocket: WebSocket连接实例
        client_id: 客户端ID
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message from client {client_id}: {data}")
            
            # 广播消息给所有连接的客户端
            await manager.broadcast(f"Client #{client_id} says: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")