"""
一点灵光 - 分镜师Agent模块
负责将剧本转化为镜头级的分镜表
"""
from typing import Dict, Any, List
import os
from app.agents.base import BaseAgent
from app.services.llm_service import llm_service


class StoryboardAgent(BaseAgent):
    """分镜师Agent：将剧本转化为镜头级分镜表"""
    
    def __init__(self):
        super().__init__(
            name="分镜师Agent",
            description="将剧本转化为镜头级的分镜表，定义镜头类型、运动方式、时长和关键帧描述"
        )
    
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行分镜任务
        
        Args:
            input_data: 包含script_data的字典
            context: 包含task_id和workspace_dir的上下文
        
        Returns:
            Dict[str, Any]: 分镜表数据
        """
        script_data = input_data.get("script_data")
        
        # 构建提示词
        prompt = self._build_prompt(script_data)
        
        # 调用LLM生成分镜
        response = llm_service.call_llm(prompt)
        
        # 解析分镜表
        storyboard_data = self._parse_storyboard_response(response)
        
        # 保存分镜表到工作目录
        task_id = context.get("task_id")
        workspace_dir = context.get("workspace_dir")
        storyboard_path = os.path.join(workspace_dir, "storyboard.json")
        
        self.save_output(storyboard_data, storyboard_path)
        
        return {
            "success": True,
            "storyboard_data": storyboard_data,
            "storyboard_path": storyboard_path
        }
    
    def _build_prompt(self, script_data: Dict[str, Any]) -> str:
        """
        构建分镜提示词
        
        Args:
            script_data: 剧本数据
        
        Returns:
            str: 构建好的提示词
        """
        import json
        script_json = json.dumps(script_data, ensure_ascii=False)
        
        return f"""你是一位专业分镜师。请根据以下剧本，生成详细的镜头分镜表。

剧本内容：
{script_json}

请生成分镜表，每个镜头包含：
- 镜头类型（远景/全景/中景/近景/特写）
- 运动方式（固定/推/拉/摇/移/跟/升降）
- 画面描述（关键帧描述）
- 时长（秒）
- 运镜说明

请以JSON格式输出，格式如下：
{{
    "total_duration": 总时长,
    "shots": [
        {{
            "shot_number": 1,
            "shot_type": "镜头类型",
            "movement": "运动方式",
            "description": "画面描述",
            "duration": 时长,
            "camera_angle": "相机角度",
            "key_frame_description": "关键帧描述"
        }}
    ]
}}

请确保分镜连贯、节奏合理，适合视频表现。"""
    
    def _parse_storyboard_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM返回的分镜表响应
        
        Args:
            response: LLM返回的文本
        
        Returns:
            Dict[str, Any]: 解析后的分镜表数据
        """
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
        except Exception as e:
            return {
                "title": "分镜生成失败",
                "error": str(e),
                "raw_response": response
            }
        
        return {
            "title": "分镜生成失败",
            "raw_response": response
        }
