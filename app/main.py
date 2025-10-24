# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import setup_logging

# 设置日志
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Mumo FastAPI项目 - 基于FastAPI的现代Web应用",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """根路径端点。
    
    Returns:
        欢迎消息
    """
    return {
        "message": f"欢迎使用 {settings.PROJECT_NAME}",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """健康检查端点。
    
    Returns:
        应用状态信息
    """
    return {"status": "healthy", "version": "1.0.0"}