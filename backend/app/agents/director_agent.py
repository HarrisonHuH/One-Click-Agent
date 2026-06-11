"""
一点灵光 - 导演Agent模块
负责统筹视觉资产规划，调用图像和视频生成API
"""
from typing import Dict, Any, List
import os
from app.agents.base import BaseAgent
from app.services.llm_service import llm_service
from app.services.image_service import image_service
from app.services.video_service import video_service


class DirectorAgent(BaseAgent):
    """导演Agent：规划视觉资产，生成画面和视频片段"""
    
    def __init__(self):
        super().__init__(
            name="导演Agent",
            description="统筹视觉资产规划，调用技能提取引擎，协调图像生成与视频生成，执行一致性校验"
        )
    
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行导演任务
        
        Args:
            input_data: 包含storyboard_data和script_data的字典
            context: 包含task_id和workspace_dir的上下文
        
        Returns:
            Dict[str, Any]: 视频片段列表
        """
        storyboard_data = input_data.get("storyboard_data")
        script_data = input_data.get("script_data")
        style = input_data.get("style", "写实")
        
        shots = storyboard_data.get("shots", [])
        video_clips = []
        reference_frames = {}  # 用于保持角色一致性的参考帧
        
        # 遍历每个镜头生成视频片段
        for idx, shot in enumerate(shots):
            shot_result = self._process_shot(
                shot=shot,
                script_data=script_data,
                style=style,
                context=context,
                reference_frames=reference_frames
            )
            video_clips.append(shot_result)
            
            # 更新参考帧（用于保持一致性）
            if shot_result.get("reference_frame"):
                character = shot.get("character", "main")
                reference_frames[character] = shot_result["reference_frame"]
        
        # 保存视频片段列表
        task_id = context.get("task_id")
        workspace_dir = context.get("workspace_dir")
        clips_path = os.path.join(workspace_dir, "video_clips.json")
        
        self.save_output({"clips": video_clips}, clips_path)
        
        return {
            "success": True,
            "video_clips": video_clips,
            "clips_path": clips_path
        }
    
    def _process_shot(
        self,
        shot: Dict[str, Any],
        script_data: Dict[str, Any],
        style: str,
        context: Dict[str, Any],
        reference_frames: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        处理单个镜头
        
        Args:
            shot: 镜头数据
            script_data: 剧本数据
            style: 视频风格
            context: 执行上下文
            reference_frames: 参考帧字典
        
        Returns:
            Dict[str, Any]: 视频片段结果
        """
        workspace_dir = context.get("workspace_dir")
        shot_number = shot.get("shot_number", 1)
        
        # 构建图像生成提示词
        prompt = self._build_image_prompt(shot, script_data, style)
        
        # 生成关键帧图像
        image_path = os.path.join(workspace_dir, f"shot_{shot_number}_image.png")
        image_result = image_service.generate_image(
            prompt=prompt,
            style=style,
            output_path=image_path
        )
        
        reference_frame = image_result.get("image_path")
        
        # 将图像扩展为视频片段
        video_path = os.path.join(workspace_dir, f"shot_{shot_number}_video.mp4")
        video_result = video_service.generate_video(
            image_path=reference_frame,
            prompt=shot.get("key_frame_description", ""),
            duration=shot.get("duration", 3),
            output_path=video_path
        )
        
        return {
            "shot_number": shot_number,
            "image_path": image_result.get("image_path"),
            "video_path": video_result.get("video_path"),
            "reference_frame": reference_frame,
            "duration": shot.get("duration", 3)
        }
    
    def _build_image_prompt(self, shot: Dict[str, Any], script_data: Dict[str, Any], style: str) -> str:
        """
        构建图像生成提示词
        
        Args:
            shot: 镜头数据
            script_data: 剧本数据
            style: 视频风格
        
        Returns:
            str: 图像生成提示词
        """
        shot_type = shot.get("shot_type", "中景")
        movement = shot.get("movement", "固定")
        description = shot.get("key_frame_description", shot.get("description", ""))
        
        # 获取场景中的角色信息
        characters = script_data.get("characters", [])
        character_desc = ""
        if characters:
            character_desc = f"角色: {', '.join([c.get('name', '') for c in characters])}"
        
        return f"""风格: {style}
镜头类型: {shot_type}
运镜方式: {movement}
{character_desc}
画面描述: {description}

请生成一张符合上述要求的图片。"""
