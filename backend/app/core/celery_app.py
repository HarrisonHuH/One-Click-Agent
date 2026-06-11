"""
一点灵光 - Celery应用配置模块
配置异步任务队列
"""
from celery import Celery
from app.config import settings

# 创建Celery应用实例
celery_app = Celery(
    "ydlg",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.video_task_worker"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 任务最大执行时间1小时
    worker_prefetch_multiplier=1,  # 每次只预取一个任务
)

# 配置任务路由
celery_app.conf.task_routes = {
    "app.workers.video_task_worker.generate_video_task": {"queue": "video_generation"},
}
