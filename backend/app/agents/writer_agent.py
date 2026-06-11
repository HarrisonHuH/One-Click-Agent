"""
一点灵光 - 编剧Agent模块
负责理解和扩展用户创意，生成结构化剧本
"""
from typing import Dict, Any
import os
from app.agents.base import BaseAgent
from app.services.llm_service import llm_service


class WriterAgent(BaseAgent):
    """编剧Agent：将用户创意扩写为结构化剧本"""
    
    def __init__(self):
        super().__init__(
            name="编剧Agent",
            description="负责理解和扩展用户创意，生成包含角色卡、场景表、对白、情节结构的完整剧本"
        )
    
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行编剧任务
        
        Args:
            input_data: 包含content(创意内容)和style(风格)的字典
            context: 包含task_id和workspace_dir的上下文
        
        Returns:
            Dict[str, Any]: 结构化剧本数据
        """
        content = input_data.get("content", "")
        style = input_data.get("style", "写实")
        target_duration = input_data.get("target_duration", 60)
        
        # 构建提示词
        prompt = self._build_prompt(content, style, target_duration)
        
        # 调用LLM生成剧本
        response = llm_service.call_llm(prompt)
        
        # 解析LLM返回的剧本
        script_data = self._parse_script_response(response)
        
        # 保存剧本到工作目录
        task_id = context.get("task_id")
        workspace_dir = context.get("workspace_dir")
        script_path = os.path.join(workspace_dir, "script.json")
        
        self.save_output(script_data, script_path)
        
        return {
            "success": True,
            "script_data": script_data,
            "script_path": script_path
        }
    
    def _build_prompt(self, content: str, style: str, target_duration: int) -> str:
        """
        构建编剧提示词
        
        Args:
            content: 用户输入的创意
            style: 视频风格
            target_duration: 目标时长(秒)
        
        Returns:
            str: 构建好的提示词
        """
        return f"""你是一位专业编剧。请根据以下创意内容，生成一个{target_duration}秒的视频剧本。

风格要求：{style}

创意内容：
{content}

请生成一个结构化的剧本，包含以下部分：
1. 角色卡：主要角色的外貌、性格、声音特点
2. 场景列表：每个场景的环境描述、对白、情绪基调
3. 情节结构：起承转合

请以JSON格式输出，格式如下：
{{
    "title": "剧本标题",
    "genre": "类型",
    "duration": 预估时长,
    "characters": [
        {{
            "name": "角色名",
            "description": "外貌特征",
            "personality": "性格特点",
            "voice": "声音特点"
        }}
    ],
    "scenes": [
        {{
            "scene_number": 1,
            "setting": "场景描述",
            "dialogue": [
                {{"character": "角色名", "text": "对白内容"}}
            ],
            "emotion": "情绪基调",
            "duration": 预估时长
        }}
    ],
    "story_arc": {{
        "setup": "开头",
        "development": "发展",
        "climax": "高潮",
        "conclusion": "结尾"
    }}
}}

请确保剧本情节连贯、角色一致、适合视频表现。"""
    
    def _parse_script_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM返回的剧本响应
        
        Args:
            response: LLM返回的文本
        
        Returns:
            Dict[str, Any]: 解析后的剧本数据
        """
        try:
            # 尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
        except Exception as e:
            # 如果解析失败，返回结构化的错误信息
            return {
                "title": "剧本生成失败",
                "error": str(e),
                "raw_response": response
            }
        
        return {
            "title": "剧本生成失败",
            "raw_response": response
        }
