# app/core/logger.py
import logging
import sys
from typing import Any

from app.core.config import settings


def setup_logging() -> None:
    """配置应用日志。"""
    
    # 创建日志格式器
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # 清除现有处理器
    root_logger.handlers.clear()
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 设置第三方库日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志器。
    
    Args:
        name: 日志器名称
        
    Returns:
        配置好的日志器实例
    """
    return logging.getLogger(name)