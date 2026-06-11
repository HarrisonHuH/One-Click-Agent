"""
一点灵光 - FastAPI主入口模块
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1 import generate, task, tasks, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建必要的目录
    os.makedirs(settings.WORKSPACE_DIR, exist_ok=True)
    os.makedirs(settings.VIDEO_STORAGE_DIR, exist_ok=True)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="一点灵光智能视频生成系统API",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(generate.router, prefix="/api/v1", tags=["生成任务"])
app.include_router(task.router, prefix="/api/v1/task", tags=["任务管理"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["任务列表"])
app.include_router(user.router, prefix="/api/v1/user", tags=["用户信息"])


@app.get("/")
async def root():
    """根路径健康检查"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}
