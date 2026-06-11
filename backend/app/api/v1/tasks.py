"""
一点灵光 - 任务列表API模块
处理历史任务的查询、删除和状态统计
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.task import (
    TaskListResponse,
    TaskListData,
    TaskListItem,
    DeleteTaskResponse
)
from app.core.task_manager import task_manager
from app.models.task import TaskStatus

router = APIRouter()


def format_duration(seconds: int) -> str:
    """将秒数格式化为 mm:ss"""
    minutes = seconds // 60
    secs = seconds % 60
    if minutes == 0:
        return f"{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


@router.get("", response_model=TaskListResponse)
async def get_task_list(
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=20, ge=1, le=100, description="每页数量"),
    status: str = Query(default="all", description="状态过滤"),
    keyword: Optional[str] = Query(default=None, description="搜索关键字")
):
    """
    获取历史任务列表
    
    Args:
        page: 页码
        limit: 每页数量
        status: 状态过滤
        keyword: 搜索关键字
    
    Returns:
        TaskListResponse: 任务列表
    """
    tasks, total, status_counts = task_manager.get_tasks(
        page=page, limit=limit, status_filter=status, keyword=keyword
    )
    
    items = []
    for task in tasks:
        status_value = task.status.value if isinstance(task.status, TaskStatus) else task.status
        mode_value = task.mode
        
        # 生成输入预览
        preview = task.input_content[:60] + "..." if len(task.input_content) > 60 else task.input_content
        
        items.append(TaskListItem(
            task_id=task.id,
            title=task.title or (task.input_content[:20] if task.input_content else "未命名项目"),
            mode=mode_value,
            mode_label=task_manager.get_mode_label(mode_value),
            input_preview=preview,
            style=task.style,
            style_tags=task.style_tags or [],
            status=status_value,
            status_label=task_manager.get_status_label(status_value),
            thumbnail_url=task.thumbnail_url,
            duration=task.target_duration,
            duration_display=format_duration(task.target_duration),
            resolution=task.resolution,
            created_at=task.created_at.isoformat() if task.created_at else "",
            updated_at=task.updated_at.isoformat() if task.updated_at else "",
            collaborators=task.collaborators or []
        ))
    
    return TaskListResponse(
        code=0,
        data=TaskListData(
            total=total,
            page=page,
            limit=limit,
            status_counts=status_counts,
            items=items
        )
    )


@router.delete("/{task_id}", response_model=DeleteTaskResponse)
async def delete_task(task_id: str, permanent: bool = False):
    """
    删除任务
    
    Args:
        task_id: 任务ID
        permanent: 是否永久删除（默认移到回收站）
    
    Returns:
        DeleteTaskResponse: 删除结果
    """
    if permanent:
        success = task_manager.permanently_delete_task(task_id)
    else:
        success = task_manager.delete_task(task_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return DeleteTaskResponse(
        code=0,
        message="任务已移至回收站" if not permanent else "任务已永久删除"
    )
