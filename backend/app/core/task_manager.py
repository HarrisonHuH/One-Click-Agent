"""
一点灵光 - 任务管理器模块
负责任务的创建、状态更新和查询
"""
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.models.task import Base, Task, TaskStatus, GenerationStage, User, GenerationLog


# ========== 阶段配置 ==========

# 6 阶段定义（与设计图一致）
STAGE_CONFIG = [
    {
        "stage": "SCRIPT_PARSING",
        "label": "剧本解析",
        "description": "解析脚本内容，提取关键信息与场景",
        "weight": 12
    },
    {
        "stage": "STORYBOARD",
        "label": "分镜处理",
        "description": "处理分镜画面，理解镜头语言",
        "weight": 10
    },
    {
        "stage": "ASSET_GENERATION",
        "label": "素材生成",
        "description": "生成画面与视频片段素材",
        "weight": 30
    },
    {
        "stage": "VIDEO_SYNTHESIS",
        "label": "视频合成",
        "description": "合成视频片段，添加转场与特效",
        "weight": 18
    },
    {
        "stage": "AUDIO_GENERATION",
        "label": "音频生成",
        "description": "生成配乐、音效与配音",
        "weight": 12
    },
    {
        "stage": "IMAGE_OPTIMIZATION",
        "label": "画面优化",
        "description": "提升画质，优化色彩与细节",
        "weight": 10
    },
    {
        "stage": "VIDEO_EXPORT",
        "label": "导出视频",
        "description": "渲染并导出最终视频文件",
        "weight": 8
    }
]

# 模式标签映射
MODE_LABELS = {
    "idea": "创意",
    "script": "剧本",
    "novel": "小说",
    "reference": "参考"
}

# 状态标签映射
STATUS_LABELS = {
    TaskStatus.DRAFT: "草稿",
    TaskStatus.PENDING: "等待中",
    TaskStatus.PROCESSING: "进行中",
    TaskStatus.SUCCESS: "已完成",
    TaskStatus.FAILED: "失败",
    TaskStatus.RECYCLED: "已回收"
}


class TaskManager:
    """任务管理器类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # 初始化默认用户
        self._init_default_user()
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()
    
    def _init_default_user(self):
        """初始化默认用户（用于演示）"""
        session = self.get_session()
        try:
            user = session.query(User).first()
            if not user:
                user = User(
                    id="default-user-001",
                    username="xiaolan",
                    nickname="小蓝鲸",
                    email="lanjing@example.com",
                    avatar_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=anime%20boy%20avatar%20cute%20chinese%20style&image_size=square",
                    bio="专注于 AI 视频创作与内容生产。",
                    credits=128.50,
                    remaining_minutes=320,
                    account_type="creator",
                    user_code="U_20240516000123"
                )
                session.add(user)
                session.commit()
        finally:
            session.close()
    
    # ========== 任务管理 ==========
    
    def create_task(
        self,
        mode: str,
        content: str,
        style: str = "电影感",
        style_tags: list = None,
        target_duration: int = 60,
        aspect_ratio: str = "16:9",
        resolution: str = "1080P"
    ) -> str:
        """
        创建新任务
        
        Args:
            mode: 生成模式
            content: 输入内容
            style: 主风格
            style_tags: 风格标签
            target_duration: 目标时长
            aspect_ratio: 画面比例
            resolution: 分辨率
        
        Returns:
            str: 任务ID
        """
        task_id = str(uuid.uuid4())
        session = self.get_session()
        try:
            # 计算预计消耗积分（按时长估算）
            credits_consumed = max(5, target_duration // 10)
            # 预计用时（分钟）
            estimated_minutes = max(1, target_duration // 30)
            
            task = Task(
                id=task_id,
                mode=mode,
                input_content=content,
                style=style,
                style_tags=style_tags or [],
                target_duration=target_duration,
                aspect_ratio=aspect_ratio,
                resolution=f"{1920 if 'P' in resolution else 1280}x{1080 if 'P' in resolution else 720}",
                status=TaskStatus.PENDING,
                current_stage=GenerationStage.PENDING,
                overall_progress=0,
                stage_progress=self._get_initial_stage_progress(),
                credits_consumed=credits_consumed,
                estimated_minutes=estimated_minutes
            )
            session.add(task)
            session.commit()
            
            # 创建任务工作目录
            task_dir = os.path.join(settings.WORKSPACE_DIR, task_id)
            os.makedirs(task_dir, exist_ok=True)
            
            # 记录初始日志
            self._add_log(
                task_id=task_id,
                stage="PENDING",
                message="任务已创建"
            )
            
            return task_id
        finally:
            session.close()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务详情"""
        session = self.get_session()
        try:
            return session.query(Task).filter(Task.id == task_id).first()
        finally:
            session.close()
    
    def update_task_status(
        self,
        task_id: str,
        status: Optional[TaskStatus] = None,
        current_stage: Optional[GenerationStage] = None,
        stage_progress: Optional[dict] = None,
        overall_progress: Optional[int] = None,
        video_url: Optional[str] = None,
        preview_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """更新任务状态"""
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
            
            if status is not None:
                task.status = status
                if status == TaskStatus.SUCCESS:
                    task.completed_at = datetime.utcnow()
            if current_stage is not None:
                task.current_stage = current_stage
            if stage_progress is not None:
                task.stage_progress = stage_progress
            if overall_progress is not None:
                task.overall_progress = overall_progress
            if video_url is not None:
                task.video_url = video_url
            if preview_url is not None:
                task.preview_url = preview_url
            if thumbnail_url is not None:
                task.thumbnail_url = thumbnail_url
            if error_message is not None:
                task.error_message = error_message
            
            task.updated_at = datetime.utcnow()
            session.commit()
            return True
        finally:
            session.close()
    
    def update_stage_status(
        self,
        task_id: str,
        stage: str,
        stage_status: str,
        progress: int = 0,
        message: Optional[str] = None
    ) -> bool:
        """更新单个阶段的状态"""
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
            
            # 更新阶段进度
            stage_progress = task.stage_progress or {}
            now = datetime.utcnow().isoformat()
            
            if stage not in stage_progress:
                stage_progress[stage] = {
                    "stage": stage,
                    "label": self._get_stage_label(stage),
                    "status": "PENDING",
                    "progress": 0
                }
            
            stage_info = stage_progress[stage]
            old_status = stage_info.get("status", "PENDING")
            stage_info["status"] = stage_status
            stage_info["progress"] = progress
            
            if stage_status == "PROCESSING" and old_status == "PENDING":
                stage_info["started_at"] = now
            if stage_status in ("COMPLETED", "FAILED"):
                stage_info["completed_at"] = now
                # 计算耗时
                if "started_at" in stage_info:
                    started = datetime.fromisoformat(stage_info["started_at"])
                    duration = (datetime.utcnow() - started).total_seconds()
                    stage_info["duration"] = int(duration)
            
            if message:
                stage_info["message"] = message
            
            stage_progress[stage] = stage_info
            task.stage_progress = stage_progress
            
            # 更新当前阶段
            if stage_status == "PROCESSING":
                task.current_stage = stage
            
            # 计算总体进度
            task.overall_progress = self._calculate_overall_progress(stage_progress)
            
            task.updated_at = datetime.utcnow()
            session.commit()
            
            # 记录日志
            self._add_log(
                task_id=task_id,
                stage=stage,
                level="ERROR" if stage_status == "FAILED" else "INFO",
                message=message or f"{self._get_stage_label(stage)} - {stage_status}",
                progress=progress
            )
            
            return True
        finally:
            session.close()
    
    def get_tasks(
        self,
        page: int = 1,
        limit: int = 20,
        status_filter: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> tuple[List[Task], int, Dict[str, int]]:
        """
        获取任务列表
        
        Args:
            page: 页码
            limit: 每页数量
            status_filter: 状态过滤
            keyword: 搜索关键字
        
        Returns:
            tuple: (任务列表, 总数, 状态统计)
        """
        session = self.get_session()
        try:
            # 获取各状态的数量
            status_counts = {}
            for status in TaskStatus:
                count = session.query(Task).filter(Task.status == status).count()
                status_counts[status.value] = count
            
            # 主查询
            query = session.query(Task)
            
            # 应用状态过滤
            if status_filter and status_filter not in ("all", "全部"):
                status_map = {
                    "draft": TaskStatus.DRAFT,
                    "pending": TaskStatus.PENDING,
                    "processing": TaskStatus.PROCESSING,
                    "success": TaskStatus.SUCCESS,
                    "failed": TaskStatus.FAILED,
                    "recycled": TaskStatus.RECYCLED,
                    "进行中": TaskStatus.PROCESSING,
                    "已完成": TaskStatus.SUCCESS,
                    "草稿": TaskStatus.DRAFT,
                    "回收站": TaskStatus.RECYCLED
                }
                if status_filter in status_map:
                    query = query.filter(Task.status == status_map[status_filter])
            
            # 关键字搜索
            if keyword:
                query = query.filter(
                    (Task.input_content.contains(keyword)) |
                    (Task.title.contains(keyword)) |
                    (Task.style.contains(keyword))
                )
            
            # 获取总数
            total = query.count()
            
            # 分页
            offset = (page - 1) * limit
            tasks = query.order_by(Task.updated_at.desc()).offset(offset).limit(limit).all()
            
            return tasks, total, status_counts
        finally:
            session.close()
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务（移到回收站）"""
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
            
            # 软删除：移到回收站
            task.status = TaskStatus.RECYCLED
            task.updated_at = datetime.utcnow()
            session.commit()
            return True
        finally:
            session.close()
    
    def permanently_delete_task(self, task_id: str) -> bool:
        """永久删除任务"""
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
            
            session.delete(task)
            session.commit()
            
            # 删除工作目录
            task_dir = os.path.join(settings.WORKSPACE_DIR, task_id)
            if os.path.exists(task_dir):
                import shutil
                shutil.rmtree(task_dir)
            
            return True
        finally:
            session.close()
    
    # ========== 用户管理 ==========
    
    def get_user(self, user_id: str = "default-user-001") -> Optional[User]:
        """获取用户信息"""
        session = self.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """更新用户信息"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            
            user.updated_at = datetime.utcnow()
            session.commit()
            return True
        finally:
            session.close()
    
    # ========== 日志管理 ==========
    
    def _add_log(
        self,
        task_id: str,
        stage: str,
        message: str,
        level: str = "INFO",
        progress: int = 0,
        duration: Optional[int] = None
    ) -> None:
        """添加生成日志"""
        session = self.get_session()
        try:
            log = GenerationLog(
                task_id=task_id,
                stage=stage,
                level=level,
                message=message,
                progress=progress,
                duration=duration
            )
            session.add(log)
            session.commit()
        finally:
            session.close()
    
    def get_logs(self, task_id: str) -> List[GenerationLog]:
        """获取任务日志"""
        session = self.get_session()
        try:
            return session.query(GenerationLog).filter(
                GenerationLog.task_id == task_id
            ).order_by(GenerationLog.created_at.asc()).all()
        finally:
            session.close()
    
    # ========== 辅助方法 ==========
    
    def _get_initial_stage_progress(self) -> dict:
        """获取初始阶段进度"""
        progress = {}
        for stage_config in STAGE_CONFIG:
            progress[stage_config["stage"]] = {
                "stage": stage_config["stage"],
                "label": stage_config["label"],
                "status": "PENDING",
                "progress": 0
            }
        return progress
    
    def _calculate_overall_progress(self, stage_progress: dict) -> int:
        """根据各阶段进度计算总体进度"""
        total_weight = sum(s["weight"] for s in STAGE_CONFIG)
        weighted_progress = 0
        
        for stage_config in STAGE_CONFIG:
            stage = stage_config["stage"]
            weight = stage_config["weight"]
            
            if stage in stage_progress:
                stage_info = stage_progress[stage]
                status = stage_info.get("status", "PENDING")
                progress = stage_info.get("progress", 0)
                
                if status == "COMPLETED":
                    weighted_progress += weight
                elif status == "PROCESSING":
                    weighted_progress += weight * (progress / 100)
        
        return int((weighted_progress / total_weight) * 100)
    
    def _get_stage_label(self, stage: str) -> str:
        """获取阶段标签"""
        for s in STAGE_CONFIG:
            if s["stage"] == stage:
                return s["label"]
        return stage
    
    def get_stage_config(self) -> list:
        """获取阶段配置"""
        return STAGE_CONFIG
    
    def get_status_label(self, status) -> str:
        """获取状态标签"""
        if isinstance(status, str):
            for s in TaskStatus:
                if s.value == status:
                    return STATUS_LABELS.get(s, status)
        return STATUS_LABELS.get(status, str(status))
    
    def get_mode_label(self, mode: str) -> str:
        """获取模式标签"""
        return MODE_LABELS.get(mode, mode)


# 全局任务管理器实例
task_manager = TaskManager()
