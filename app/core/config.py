# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类，使用Pydantic Settings管理环境变量。"""
    
    PROJECT_NAME: str = "Mumo FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./mumo_fastapi.db"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()