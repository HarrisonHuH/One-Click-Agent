"""
一点灵光 - LLM服务模块
封装大语言模型API调用
"""
from typing import Optional, Dict, Any
import os
from app.config import settings


class LLMService:
    """LLM服务类"""
    
    def __init__(self):
        """初始化LLM服务"""
        self.api_key = settings.LLM_API_KEY or os.environ.get("OPENAI_API_KEY")
        self.base_url = settings.LLM_BASE_URL
        self.model = settings.LLM_MODEL
    
    def call_llm(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        调用LLM生成内容
        
        Args:
            prompt: 输入提示词
            temperature: 温度参数（控制随机性）
            max_tokens: 最大生成的token数
        
        Returns:
            str: LLM生成的文本
        """
        # 模拟实现，实际使用时需要接入真实的LLM API
        # 这里可以接入OpenAI GPT-4、Google Gemini等
        
        if not self.api_key:
            # 如果没有API密钥，返回模拟数据用于开发测试
            return self._generate_mock_response(prompt)
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的编剧和导演，擅长创作视频剧本和分镜表。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM调用失败: {str(e)}")
            return self._generate_mock_response(prompt)
    
    def _generate_mock_response(self, prompt: str) -> str:
        """
        生成模拟响应（用于开发测试）
        
        Args:
            prompt: 输入提示词
        
        Returns:
            str: 模拟的响应内容
        """
        # 根据提示词类型返回相应的模拟数据
        if "剧本" in prompt:
            return """{
    "title": "猫狗奇遇记",
    "genre": "动画/喜剧",
    "duration": 60,
    "characters": [
        {
            "name": "旺财",
            "description": "黄色的土狗，体型中等，忠诚友善",
            "personality": "忠诚、勇敢、有点贪吃",
            "voice": "温和的男声"
        },
        {
            "name": "喵喵",
            "description": "白色的猫咪，体型小巧，优雅敏捷",
            "personality": "聪明、好奇、有点傲娇",
            "voice": "清脆的女声"
        }
    ],
    "scenes": [
        {
            "scene_number": 1,
            "setting": "阳光明媚的小区花园，鲜花盛开",
            "dialogue": [
                {"character": "旺财", "text": "喵喵，今天天气真好呀！"},
                {"character": "喵喵", "text": "是呀，适合出去探险呢！"}
            ],
            "emotion": "欢快、期待",
            "duration": 15
        },
        {
            "scene_number": 2,
            "setting": "花园角落发现了一个新来的猫咪",
            "dialogue": [
                {"character": "旺财", "text": "那边有只新来的猫，我们去看看吧！"},
                {"character": "喵喵", "text": "好啊好啊！"}
            ],
            "emotion": "好奇、兴奋",
            "duration": 20
        },
        {
            "scene_number": 3,
            "setting": "三只小动物成为了好朋友",
            "dialogue": [
                {"character": "旺财", "text": "欢迎你加入我们！"},
                {"character": "喵喵", "text": "以后我们一起玩吧！"}
            ],
            "emotion": "温馨、欢乐",
            "duration": 25
        }
    ],
    "story_arc": {
        "setup": "旺财和喵喵在花园玩耍",
        "development": "发现了一只新来的猫咪",
        "climax": "三只动物互相介绍，成为朋友",
        "conclusion": "他们约定一起开始新的冒险"
    }
}"""
        elif "分镜" in prompt:
            return """{
    "total_duration": 60,
    "shots": [
        {
            "shot_number": 1,
            "shot_type": "全景",
            "movement": "固定",
            "description": "阳光明媚的小区花园，鲜花盛开，旺财和喵喵在草地上玩耍",
            "duration": 5,
            "camera_angle": "高角度俯拍",
            "key_frame_description": "花园全景，阳光充足，两只小动物在草地上追逐嬉戏"
        },
        {
            "shot_number": 2,
            "shot_type": "中景",
            "movement": "跟拍",
            "description": "旺财和喵喵面对面聊天",
            "duration": 10,
            "camera_angle": "平视",
            "key_frame_description": "两只动物表情生动，尾巴摇摆"
        },
        {
            "shot_number": 3,
            "shot_type": "近景",
            "movement": "推",
            "description": "旺财指向花园角落",
            "duration": 5,
            "camera_angle": "低角度仰拍",
            "key_frame_description": "旺财表情兴奋，指向远方"
        },
        {
            "shot_number": 4,
            "shot_type": "中景",
            "movement": "移",
            "description": "三只动物聚在一起",
            "duration": 15,
            "camera_angle": "平视",
            "key_frame_description": "三只小动物围成一圈，画面温馨"
        },
        {
            "shot_number": 5,
            "shot_type": "全景",
            "movement": "拉",
            "description": "三只动物一起跑向远方",
            "duration": 10,
            "camera_angle": "低角度",
            "key_frame_description": "三只动物奔跑的剪影，夕阳西下"
        }
    ]
}"""
        else:
            return "好的，我已经理解了您的要求，正在处理..."


# 全局LLM服务实例
llm_service = LLMService()
