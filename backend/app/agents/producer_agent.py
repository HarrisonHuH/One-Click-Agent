"""
一点灵光 - 制片人Agent模块
负责编排镜头生产流水线，执行最终视频合成
"""
from typing import Dict, Any, List
import os
import subprocess
from app.agents.base import BaseAgent


class ProducerAgent(BaseAgent):
    """制片人Agent：编排镜头生产流水线，执行最终视频合成"""
    
    def __init__(self):
        super().__init__(
            name="制片人Agent",
            description="编排并行化的镜头生产流水线，执行多维质量评估，管理资源分配与异常处理，完成最终合成"
        )
    
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行制片任务
        
        Args:
            input_data: 包含video_clips的字典
            context: 包含task_id和workspace_dir的上下文
        
        Returns:
            Dict[str, Any]: 最终视频文件路径
        """
        video_clips = input_data.get("video_clips", [])
        workspace_dir = context.get("workspace_dir")
        
        # 创建最终视频路径
        final_video_path = os.path.join(workspace_dir, "final.mp4")
        
        # 拼接视频片段
        concat_list_path = self._create_concat_list(video_clips, workspace_dir)
        
        # 使用FFmpeg拼接视频
        success = self._concat_videos(concat_list_path, final_video_path)
        
        if not success:
            return {
                "success": False,
                "error": "视频拼接失败"
            }
        
        return {
            "success": True,
            "final_video_path": final_video_path
        }
    
    def _create_concat_list(self, video_clips: List[Dict[str, Any]], workspace_dir: str) -> str:
        """
        创建FFmpeg拼接列表文件
        
        Args:
            video_clips: 视频片段列表
            workspace_dir: 工作目录
        
        Returns:
            str: 拼接列表文件路径
        """
        concat_list_path = os.path.join(workspace_dir, "concat_list.txt")
        
        with open(concat_list_path, 'w', encoding='utf-8') as f:
            for clip in video_clips:
                video_path = clip.get("video_path", "")
                # FFmpeg需要绝对路径或正确的相对路径
                if not os.path.isabs(video_path):
                    video_path = os.path.join(workspace_dir, video_path)
                f.write(f"file '{video_path}'\n")
        
        return concat_list_path
    
    def _concat_videos(self, concat_list_path: str, output_path: str) -> bool:
        """
        使用FFmpeg拼接视频
        
        Args:
            concat_list_path: 拼接列表文件路径
            output_path: 输出文件路径
        
        Returns:
            bool: 是否成功
        """
        try:
            # FFmpeg拼接命令
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_list_path,
                "-c", "copy",
                "-y",  # 覆盖已存在的文件
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            return result.returncode == 0
        except Exception as e:
            print(f"FFmpeg拼接失败: {str(e)}")
            return False
    
    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        volume: float = 0.5
    ) -> bool:
        """
        为视频添加背景音乐
        
        Args:
            video_path: 视频路径
            audio_path: 音频路径
            output_path: 输出路径
            volume: 音量大小
        
        Returns:
            bool: 是否成功
        """
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-filter_complex",
                f"[1:a]volume={volume}[a]",
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return result.returncode == 0
        except Exception as e:
            print(f"添加音频失败: {str(e)}")
            return False
    
    def add_subtitles(
        self,
        video_path: str,
        subtitles_path: str,
        output_path: str
    ) -> bool:
        """
        为视频添加字幕
        
        Args:
            video_path: 视频路径
            subtitles_path: 字幕文件路径(SRT格式)
            output_path: 输出路径
        
        Returns:
            bool: 是否成功
        """
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf",
                f"subtitles={subtitles_path}",
                "-c:a", "copy",
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return result.returncode == 0
        except Exception as e:
            print(f"添加字幕失败: {str(e)}")
            return False
