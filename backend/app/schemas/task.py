"""
一点灵光 - Pydantic请求/响应模型模块
定义API请求和响应的数据结构
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime


# ========== 创作生成相关 ==========

class GenerateRequest(BaseModel):
    """提交生成任务的请求模型"""
    mode: Literal["idea", "script", "novel", "reference"] = Field(
        default="idea", description="生成模式"
    )
    content: str = Field(..., min_length=1, max_length=10000, description="输入内容")
    style: str = Field(default="电影感", description="视频风格")
    style_tags: List[str] = Field(default_factory=list, description="风格标签")
    target_duration: int = Field(default=60, ge=15, le=300, description="目标时长(秒)")
    aspect_ratio: Literal["16:9", "9:16", "1:1", "4:3", "3:4"] = Field(
        default="16:9", description="画面比例"
    )
    resolution: str = Field(default="1080P", description="分辨率")
    reference_url: Optional[str] = Field(default=None, description="参考图/视频URL")

    class Config:
        json_schema_extra = {
            "example": {
                "mode": "idea",
                "content": "一个年轻人在雨夜的街头遇到一只流浪猫...",
                "style": "电影感",
                "style_tags": ["温馨", "治愈", "情感"],
                "target_duration": 60,
                "aspect_ratio": "16:9",
                "resolution": "1080P"
            }
        }


class GenerateResponse(BaseModel):
    """提交生成任务的响应模型"""
    code: int = 0
    message: str = "success"
    data: dict = Field(default_factory=dict)


# ========== 任务状态相关 ==========

class StageProgress(BaseModel):
    """单个阶段的进度信息"""
    stage: str
    label: str
    status: str  # PENDING/PROCESSING/COMPLETED/FAILED
    progress: int = 0
    duration: Optional[int] = None  # 耗时(秒)
    message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class TaskStatusData(BaseModel):
    """任务状态详情"""
    task_id: str
    title: Optional[str] = None
    status: str
    overall_progress: int
    current_stage: str
    current_stage_label: str
    stage_progress: Dict[str, StageProgress]
    video_url: Optional[str] = None
    preview_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error_message: Optional[str] = None
    credits_consumed: int = 0
    estimated_remaining_minutes: int = 0


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    code: int = 0
    data: TaskStatusData


# ========== 任务列表相关 ==========

class TaskListItem(BaseModel):
    """任务列表项"""
    task_id: str
    title: str
    mode: str
    mode_label: str
    input_preview: str
    style: str
    style_tags: List[str]
    status: str
    status_label: str
    thumbnail_url: Optional[str] = None
    duration: int
    duration_display: str
    resolution: str
    created_at: str
    updated_at: str
    collaborators: List[str] = Field(default_factory=list)


class TaskListData(BaseModel):
    """任务列表数据"""
    total: int
    page: int
    limit: int
    status_counts: Dict[str, int]
    items: List[TaskListItem]


class TaskListResponse(BaseModel):
    """任务列表响应"""
    code: int = 0
    data: TaskListData


class DeleteTaskResponse(BaseModel):
    """删除任务响应"""
    code: int = 0
    message: str = "success"


# ========== 用户相关 ==========

class UserInfo(BaseModel):
    """用户信息"""
    user_id: str
    username: str
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    credits: float
    remaining_minutes: int
    account_type: str
    user_code: Optional[str] = None


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    code: int = 0
    data: UserInfo


class UserUpdateRequest(BaseModel):
    """用户信息更新请求"""
    nickname: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


# ========== 生成日志相关 ==========

class GenerationLogItem(BaseModel):
    """生成日志项"""
    id: int
    stage: str
    level: str
    message: str
    progress: int
    created_at: str


class GenerationLogResponse(BaseModel):
    """生成日志响应"""
    code: int = 0
    data: List[GenerationLogItem]
