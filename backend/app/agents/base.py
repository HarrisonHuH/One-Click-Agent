"""
一点灵光 - Agent基类模块
定义所有智能体的通用接口和功能
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json


class BaseAgent(ABC):
    """智能体基类，定义通用接口"""
    
    def __init__(self, name: str, description: str):
        """
        初始化智能体
        
        Args:
            name: 智能体名称
            description: 智能体功能描述
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据并返回结果
        
        Args:
            input_data: 输入数据字典
            context: 执行上下文（包含任务ID、工作目录等）
        
        Returns:
            Dict[str, Any]: 处理结果
        """
        pass
    
    def save_output(self, output_data: Dict[str, Any], file_path: str) -> str:
        """
        将输出数据保存到JSON文件
        
        Args:
            output_data: 输出数据
            file_path: 文件路径
        
        Returns:
            str: 保存的文件路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        return file_path
    
    def load_input(self, file_path: str) -> Dict[str, Any]:
        """
        从JSON文件加载输入数据
        
        Args:
            file_path: 文件路径
        
        Returns:
            Dict[str, Any]: 加载的数据
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_output(self, output: Dict[str, Any], required_keys: list) -> bool:
        """
        验证输出是否包含必需的键
        
        Args:
            output: 输出数据
            required_keys: 必需的键列表
        
        Returns:
            bool: 是否通过验证
        """
        for key in required_keys:
            if key not in output:
                return False
        return True
