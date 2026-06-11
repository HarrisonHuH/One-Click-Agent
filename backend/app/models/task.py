"""
一点灵光 - 任务数据模型模块
定义任务相关的数据库模型
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, Float, Enum as SQLEnum, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class TaskStatus(str, enum.Enum):
    """任务状态枚举"""
    DRAFT = "DRAFT"           # 草稿
    PENDING = "PENDING"       # 等待处理
    PROCESSING = "PROCESSING" # 处理中
    SUCCESS = "SUCCESS"       # 成功
    FAILED = "FAILED"         # 失败
    RECYCLED = "RECYCLED"     # 已回收


class GenerationStage(str, enum.Enum):
    """生成阶段枚举 - 6 阶段"""
    PENDING = "PENDING"                       # 等待开始
    SCRIPT_PARSING = "SCRIPT_PARSING"         # 剧本解析
    STORYBOARD = "STORYBOARD"                 # 分镜处理
    ASSET_GENERATION = "ASSET_GENERATION"     # 素材生成
    VIDEO_SYNTHESIS = "VIDEO_SYNTHESIS"       # 视频合成
    AUDIO_GENERATION = "AUDIO_GENERATION"     # 音频生成
    IMAGE_OPTIMIZATION = "IMAGE_OPTIMIZATION" # 画面优化
    VIDEO_EXPORT = "VIDEO_EXPORT"             # 导出视频
    COMPLETED = "COMPLETED"                   # 已完成


class Task(Base):
    """任务数据模型 - 视频创作项目"""
    __tablename__ = "tasks"

    # 基础字段
    id = Column(String(36), primary_key=True)  # UUID格式的任务ID
    title = Column(String(200), nullable=True)  # 项目标题
    mode = Column(String(20), nullable=False)  # 生成模式：idea/script/novel/reference
    input_content = Column(Text, nullable=False)  # 输入内容
    style = Column(String(50), nullable=False)  # 主风格
    style_tags = Column(JSON, default=list)  # 风格标签数组
    target_duration = Column(Integer, nullable=False)  # 目标时长(秒)
    aspect_ratio = Column(String(10), default="16:9")  # 画面比例
    
    # 状态字段
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    current_stage = Column(SQLEnum(GenerationStage), default=GenerationStage.PENDING)
    stage_progress = Column(JSON, default=dict)  # 各阶段进度
    overall_progress = Column(Integer, default=0)  # 总进度 0-100
    
    # 资源字段
    thumbnail_url = Column(String(500), nullable=True)  # 缩略图URL
    video_url = Column(String(500), nullable=True)  # 视频URL
    preview_url = Column(String(500), nullable=True)  # 实时预览URL
    
    # 视频元数据
    resolution = Column(String(20), default="1920x1080")  # 分辨率
    file_size = Column(Integer, nullable=True)  # 文件大小(字节)
    
    # 错误信息
    error_message = Column(Text, nullable=True)
    
    # 积分消耗
    credits_consumed = Column(Integer, default=0)  # 消耗积分
    estimated_minutes = Column(Integer, default=0)  # 预计用时(分钟)
    
    # 协作
    collaborators = Column(JSON, default=list)  # 协作者列表
    
    # 时间字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        """转换为字典格式"""
        return {
            "task_id": self.id,
            "title": self.title or self._generate_title(),
            "mode": self.mode,
            "input_content": self.input_content,
            "input_preview": self.input_content[:50] + "..." if len(self.input_content) > 50 else self.input_content,
            "style": self.style,
            "style_tags": self.style_tags or [],
            "target_duration": self.target_duration,
            "aspect_ratio": self.aspect_ratio,
            "status": self.status.value if isinstance(self.status, TaskStatus) else self.status,
            "current_stage": self.current_stage.value if isinstance(self.current_stage, GenerationStage) else self.current_stage,
            "stage_progress": self.stage_progress or {},
            "overall_progress": self.overall_progress,
            "thumbnail_url": self.thumbnail_url,
            "video_url": self.video_url,
            "preview_url": self.preview_url,
            "resolution": self.resolution,
            "file_size": self.file_size,
            "error_message": self.error_message,
            "credits_consumed": self.credits_consumed,
            "estimated_minutes": self.estimated_minutes,
            "collaborators": self.collaborators or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def _generate_title(self) -> str:
        """从输入内容生成标题"""
        if not self.input_content:
            return "未命名项目"
        return self.input_content[:20] + ("..." if len(self.input_content) > 20 else "")


class User(Base):
    """用户数据模型"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    nickname = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # 账户信息
    credits = Column(Float, default=0.0)  # 账户余额
    remaining_minutes = Column(Integer, default=0)  # 剩余生成时长(分钟)
    account_type = Column(String(20), default="free")  # 账户类型: free/creator/professional
    user_code = Column(String(50), unique=True, nullable=True)  # 用户ID
    
    # 偏好设置
    preferences = Column(JSON, default=dict)
    
    # 时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "user_id": self.id,
            "username": self.username,
            "nickname": self.nickname or self.username,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "credits": self.credits,
            "remaining_minutes": self.remaining_minutes,
            "account_type": self.account_type,
            "user_code": self.user_code,
            "preferences": self.preferences or {},
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class GenerationLog(Base):
    """生成日志 - 记录每个阶段的执行情况"""
    __tablename__ = "generation_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(36), nullable=False, index=True)
    stage = Column(String(50), nullable=False)
    level = Column(String(20), default="INFO")  # INFO/WARNING/ERROR
    message = Column(Text, nullable=False)
    progress = Column(Integer, default=0)  # 该阶段进度 0-100
    duration = Column(Integer, nullable=True)  # 耗时(秒)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "stage": self.stage,
            "level": self.level,
            "message": self.message,
            "progress": self.progress,
            "duration": self.duration,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
