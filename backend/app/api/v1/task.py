"""
一点灵光 - 任务状态与结果API模块
处理单个任务的查询和结果获取
"""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.task import (
    TaskStatusResponse,
    TaskStatusData,
    StageProgress,
    GenerationLogResponse,
    GenerationLogItem
)
from app.core.task_manager import task_manager
from app.models.task import TaskStatus, GenerationStage
from app.config import settings

router = APIRouter()


@router.get("/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    获取任务状态（多阶段进度）
    
    Args:
        task_id: 任务ID
    
    Returns:
        TaskStatusResponse: 任务状态详情
    """
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 获取状态值
    status_value = task.status.value if isinstance(task.status, TaskStatus) else task.status
    current_stage = task.current_stage.value if isinstance(task.current_stage, GenerationStage) else task.current_stage
    current_stage_label = next(
        (s["label"] for s in task_manager.get_stage_config() if s["stage"] == current_stage),
        current_stage
    )
    
    # 构建阶段进度
    stage_progress = {}
    raw_stages = task.stage_progress or {}
    
    # 确保所有阶段都有数据（即便未开始）
    for stage_config in task_manager.get_stage_config():
        stage_key = stage_config["stage"]
        if stage_key in raw_stages:
            info = raw_stages[stage_key]
            stage_progress[stage_key] = StageProgress(
                stage=stage_key,
                label=info.get("label", stage_config["label"]),
                status=info.get("status", "PENDING"),
                progress=info.get("progress", 0),
                duration=info.get("duration"),
                message=info.get("message"),
                started_at=info.get("started_at"),
                completed_at=info.get("completed_at")
            )
        else:
            stage_progress[stage_key] = StageProgress(
                stage=stage_key,
                label=stage_config["label"],
                status="PENDING",
                progress=0
            )
    
    # 计算预计剩余时间
    if status_value == "PROCESSING" and task.estimated_minutes:
        # 按剩余进度比例计算
        remaining = max(1, int(task.estimated_minutes * (100 - task.overall_progress) / 100))
    else:
        remaining = 0
    
    return TaskStatusResponse(
        code=0,
        data=TaskStatusData(
            task_id=task.id,
            title=task.title or (task.input_content[:20] if task.input_content else None),
            status=status_value,
            overall_progress=task.overall_progress,
            current_stage=current_stage,
            current_stage_label=current_stage_label,
            stage_progress=stage_progress,
            video_url=task.video_url,
            preview_url=task.preview_url,
            thumbnail_url=task.thumbnail_url,
            error_message=task.error_message,
            credits_consumed=task.credits_consumed,
            estimated_remaining_minutes=remaining
        )
    )


@router.get("/{task_id}/result")
async def get_task_result(task_id: str):
    """
    获取任务生成的视频文件
    
    Args:
        task_id: 任务ID
    
    Returns:
        FileResponse: 视频文件流
    """
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != TaskStatus.SUCCESS:
        raise HTTPException(status_code=400, detail="Task not completed yet")
    
    if not task.video_url:
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # 解析视频文件路径
    video_path = task.video_url
    if not os.path.isabs(video_path):
        video_path = os.path.join(settings.VIDEO_STORAGE_DIR, video_path)
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=f"{task_id}.mp4"
    )


@router.get("/{task_id}/thumbnail")
async def get_task_thumbnail(task_id: str):
    """获取任务缩略图"""
    task = task_manager.get_task(task_id)
    if not task or not task.thumbnail_url:
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    
    thumbnail_path = task.thumbnail_url
    if not os.path.isabs(thumbnail_path):
        thumbnail_path = os.path.join(settings.VIDEO_STORAGE_DIR, thumbnail_path)
    
    if not os.path.exists(thumbnail_path):
        raise HTTPException(status_code=404, detail="Thumbnail file not found")
    
    return FileResponse(path=thumbnail_path, media_type="image/jpeg")


@router.get("/{task_id}/logs", response_model=GenerationLogResponse)
async def get_task_logs(task_id: str):
    """
    获取任务的生成日志
    
    Args:
        task_id: 任务ID
    
    Returns:
        GenerationLogResponse: 生成日志列表
    """
    logs = task_manager.get_logs(task_id)
    return GenerationLogResponse(
        code=0,
        data=[
            GenerationLogItem(
                id=log.id,
                stage=log.stage,
                level=log.level,
                message=log.message,
                progress=log.progress,
                created_at=log.created_at.isoformat() if log.created_at else ""
            )
            for log in logs
        ]
    )
