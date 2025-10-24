# app/api/v1/router.py
from fastapi import APIRouter

from app.api.v1.routes import items, ws

api_router = APIRouter()

# 包含各个路由模块
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ws.router, prefix="/websocket", tags=["websocket"])