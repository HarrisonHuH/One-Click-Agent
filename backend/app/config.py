"""
一点灵光 - 应用配置模块
管理所有环境配置和全局设置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基本信息
    APP_NAME: str = "一点灵光"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./ydlg.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # LLM API配置
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4"
    
    # 图像生成API配置
    IMAGE_API_KEY: Optional[str] = None
    IMAGE_API_BASE: str = "https://api.midjourney.com/v1"
    
    # 视频生成API配置
    VIDEO_API_KEY: Optional[str] = None
    VIDEO_API_BASE: str = "https://api.runwayml.com/v1"
    
    # 文件存储路径
    WORKSPACE_DIR: str = "./workspace"
    VIDEO_STORAGE_DIR: str = "./storage/videos"
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取缓存的配置实例"""
    return Settings()


settings = get_settings()
