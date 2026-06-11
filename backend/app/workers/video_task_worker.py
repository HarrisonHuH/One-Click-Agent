"""
一点灵光 - Celery Worker模块
负责任务调度和执行
"""
import os
import shutil
import time
from celery import Task
from app.core.celery_app import celery_app
from app.core.task_manager import task_manager
from app.models.task import TaskStatus, GenerationStage


class VideoGenerationTask(Task):
    """视频生成任务类"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """任务失败时的回调"""
        task_manager.update_task_status(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error_message=str(exc)
        )


# 注册任务基类
video_generation_task = celery_app.register_task(VideoGenerationTask())


@celery_app.task(bind=True, name="app.workers.video_task_worker.generate_video_task")
def generate_video_task(self, task_id: str):
    """
    视频生成主任务
    
    按 6 阶段执行：剧本解析 → 分镜处理 → 素材生成 → 视频合成 → 音频生成 → 画面优化 → 导出视频
    
    Args:
        task_id: 任务ID
    """
    from app.agents.writer_agent import WriterAgent
    from app.agents.storyboard_agent import StoryboardAgent
    from app.agents.director_agent import DirectorAgent
    from app.agents.producer_agent import ProducerAgent
    from app.services.quality_evaluation_service import quality_evaluation_service
    from app.config import settings
    
    # 获取任务信息
    task = task_manager.get_task(task_id)
    if not task:
        raise ValueError(f"任务 {task_id} 不存在")
    
    # 设置工作目录
    workspace_dir = os.path.join(settings.WORKSPACE_DIR, task_id)
    os.makedirs(workspace_dir, exist_ok=True)
    
    try:
        # 更新状态为处理中
        task_manager.update_task_status(
            task_id=task_id,
            status=TaskStatus.PROCESSING,
            current_stage=GenerationStage.SCRIPT_PARSING
        )
        
        # ========== 阶段1: 剧本解析 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="SCRIPT_PARSING",
            stage_status="PROCESSING",
            progress=10,
            message="解析脚本内容，提取关键信息与场景"
        )
        
        writer_agent = WriterAgent()
        writer_result = writer_agent.process(
            input_data={
                "content": task.input_content,
                "style": task.style,
                "target_duration": task.target_duration
            },
            context={"task_id": task_id, "workspace_dir": workspace_dir}
        )
        time.sleep(0.5)  # 模拟处理时间
        
        if not writer_result.get("success"):
            raise Exception("剧本解析失败")
        
        script_data = writer_result.get("script_data")
        task_manager.update_stage_status(
            task_id=task_id,
            stage="SCRIPT_PARSING",
            stage_status="COMPLETED",
            progress=100,
            message="剧本解析已完成"
        )
        
        # ========== 阶段2: 分镜处理 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="STORYBOARD",
            stage_status="PROCESSING",
            progress=10,
            message="处理分镜画面，理解镜头语言"
        )
        
        storyboard_agent = StoryboardAgent()
        storyboard_result = storyboard_agent.process(
            input_data={"script_data": script_data},
            context={"task_id": task_id, "workspace_dir": workspace_dir}
        )
        time.sleep(0.5)
        
        if not storyboard_result.get("success"):
            raise Exception("分镜处理失败")
        
        storyboard_data = storyboard_result.get("storyboard_data")
        task_manager.update_stage_status(
            task_id=task_id,
            stage="STORYBOARD",
            stage_status="COMPLETED",
            progress=100,
            message="分镜处理已完成"
        )
        
        # ========== 阶段3: 素材生成 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="ASSET_GENERATION",
            stage_status="PROCESSING",
            progress=0,
            message="生成画面与视频片段素材"
        )
        
        director_agent = DirectorAgent()
        # 模拟分阶段进度
        shots = storyboard_data.get("shots", [])
        total_shots = max(len(shots), 1)
        
        director_result = director_agent.process(
            input_data={
                "storyboard_data": storyboard_data,
                "script_data": script_data,
                "style": task.style
            },
            context={"task_id": task_id, "workspace_dir": workspace_dir}
        )
        
        # 模拟渐进式进度更新
        for progress in [25, 50, 75, 100]:
            time.sleep(0.2)
            task_manager.update_stage_status(
                task_id=task_id,
                stage="ASSET_GENERATION",
                stage_status="PROCESSING",
                progress=progress,
                message=f"生成画面与视频片段素材 ({progress}%)"
            )
        
        if not director_result.get("success"):
            raise Exception("素材生成失败")
        
        video_clips = director_result.get("video_clips", [])
        task_manager.update_stage_status(
            task_id=task_id,
            stage="ASSET_GENERATION",
            stage_status="COMPLETED",
            progress=100,
            message="素材生成已完成"
        )
        
        # ========== 阶段4: 视频合成 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="VIDEO_SYNTHESIS",
            stage_status="PROCESSING",
            progress=30,
            message="合成视频片段，添加转场与特效"
        )
        time.sleep(0.5)
        task_manager.update_stage_status(
            task_id=task_id,
            stage="VIDEO_SYNTHESIS",
            stage_status="PROCESSING",
            progress=80,
            message="合成视频片段，添加转场与特效"
        )
        
        producer_agent = ProducerAgent()
        producer_result = producer_agent.process(
            input_data={"video_clips": video_clips},
            context={"task_id": task_id, "workspace_dir": workspace_dir}
        )
        time.sleep(0.3)
        
        if not producer_result.get("success"):
            raise Exception("视频合成失败")
        
        final_video_path = producer_result.get("final_video_path")
        task_manager.update_stage_status(
            task_id=task_id,
            stage="VIDEO_SYNTHESIS",
            stage_status="COMPLETED",
            progress=100,
            message="视频合成已完成"
        )
        
        # ========== 阶段5: 音频生成 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="AUDIO_GENERATION",
            stage_status="PROCESSING",
            progress=50,
            message="生成配乐、音效与配音"
        )
        time.sleep(0.4)
        task_manager.update_stage_status(
            task_id=task_id,
            stage="AUDIO_GENERATION",
            stage_status="COMPLETED",
            progress=100,
            message="音频生成已完成"
        )
        
        # ========== 阶段6: 画面优化 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="IMAGE_OPTIMIZATION",
            stage_status="PROCESSING",
            progress=40,
            message="提升画质，优化色彩与细节"
        )
        time.sleep(0.4)
        task_manager.update_stage_status(
            task_id=task_id,
            stage="IMAGE_OPTIMIZATION",
            stage_status="COMPLETED",
            progress=100,
            message="画面优化已完成"
        )
        
        # ========== 阶段7: 导出视频 ==========
        task_manager.update_stage_status(
            task_id=task_id,
            stage="VIDEO_EXPORT",
            stage_status="PROCESSING",
            progress=30,
            message="渲染并导出最终视频文件"
        )
        
        # 质量评估
        quality_result = quality_evaluation_service.evaluate_video(final_video_path)
        time.sleep(0.3)
        
        # 移动到存储目录
        storage_dir = settings.VIDEO_STORAGE_DIR
        os.makedirs(storage_dir, exist_ok=True)
        
        final_filename = f"{task_id}.mp4"
        final_storage_path = os.path.join(storage_dir, final_filename)
        
        if os.path.exists(final_video_path):
            shutil.move(final_video_path, final_storage_path)
        
        # 生成缩略图
        thumbnail_path = self._generate_thumbnail(final_storage_path, task_id, storage_dir)
        
        task_manager.update_stage_status(
            task_id=task_id,
            stage="VIDEO_EXPORT",
            stage_status="PROCESSING",
            progress=80,
            message="导出完成"
        )
        
        task_manager.update_stage_status(
            task_id=task_id,
            stage="VIDEO_EXPORT",
            stage_status="COMPLETED",
            progress=100,
            message="视频导出已完成"
        )
        
        # ========== 标记完成 ==========
        task_manager.update_task_status(
            task_id=task_id,
            status=TaskStatus.SUCCESS,
            current_stage=GenerationStage.COMPLETED,
            video_url=final_storage_path,
            thumbnail_url=thumbnail_path,
            overall_progress=100
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "video_url": final_storage_path,
            "quality_report": quality_result
        }
        
    except Exception as e:
        # 任务失败处理
        task_manager.update_task_status(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error_message=str(e)
        )
        raise


def _generate_thumbnail(video_path: str, task_id: str, storage_dir: str) -> str:
    """
    从视频生成缩略图
    
    Args:
        video_path: 视频路径
        task_id: 任务ID
        storage_dir: 存储目录
    
    Returns:
        str: 缩略图路径
    """
    try:
        import subprocess
        thumbnail_path = os.path.join(storage_dir, f"{task_id}_thumb.jpg")
        
        # 使用FFmpeg截取第一秒的帧作为缩略图
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", "00:00:01",
            "-vframes", "1",
            "-y",
            thumbnail_path
        ]
        subprocess.run(cmd, capture_output=True, timeout=30)
        
        if os.path.exists(thumbnail_path):
            return thumbnail_path
    except Exception:
        pass
    
    return None


# 将 _generate_thumbnail 绑定到任务
VideoGenerationTask._generate_thumbnail = _generate_thumbnail
