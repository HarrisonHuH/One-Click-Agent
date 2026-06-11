"""
一点灵光 - 生成任务API模块
处理视频生成任务的提交
"""
from fastapi import APIRouter
from app.schemas.task import GenerateRequest, GenerateResponse
from app.core.task_manager import task_manager
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def submit_generate_task(request: GenerateRequest):
    """
    提交视频生成任务
    
    Args:
        request: 包含生成参数的请求体
    
    Returns:
        GenerateResponse: 包含task_id的响应
    """
    # 创建任务记录
    task_id = task_manager.create_task(
        mode=request.mode,
        content=request.content,
        style=request.style,
        style_tags=request.style_tags,
        target_duration=request.target_duration,
        aspect_ratio=request.aspect_ratio,
        resolution=request.resolution
    )
    
    # 将任务发送到Celery队列异步执行
    celery_app.send_task(
        "app.workers.video_task_worker.generate_video_task",
        args=[task_id],
        task_id=task_id
    )
    
    return GenerateResponse(
        code=0,
        message="success",
        data={"task_id": task_id}
    )
