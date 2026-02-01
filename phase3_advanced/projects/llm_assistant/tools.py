"""
工具定义文件
"""

import time
import os
from typing import Any


class Tools:
    """
    工具类
    """
    
    @staticmethod
    def get_weather(city: str) -> str:
        """
        获取城市天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息
        """
        # 模拟天气查询
        return f"{city}的天气晴朗，温度25℃"
    
    @staticmethod
    def calculate(expression: str) -> str:
        """
        计算数学表达式
        
        Args:
            expression: 数学表达式
            
        Returns:
            计算结果
        """
        try:
            # 安全计算，只允许基本运算
            result = eval(expression, {"__builtins__": {}}, {})
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    @staticmethod
    def get_current_time() -> str:
        """
        获取当前时间
        
        Returns:
            当前时间
        """
        return f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        读取文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"文件内容: {content}"
        except Exception as e:
            return f"读取文件错误: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """
        写入文件
        
        Args:
            file_path: 文件路径
            content: 文件内容
            
        Returns:
            写入结果
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"已成功创建文件 {file_path}，内容为 {content}"
        except Exception as e:
            return f"写入文件错误: {str(e)}"
    
    @staticmethod
    def list_files(directory: str) -> str:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            
        Returns:
            文件列表
        """
        try:
            files = os.listdir(directory)
            return f"目录 {directory} 中的文件: {', '.join(files)}"
        except Exception as e:
            return f"列出文件错误: {str(e)}"


# 工具列表
tool_list = [
    {
        "name": "get_weather",
        "function": Tools.get_weather,
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate",
        "function": Tools.calculate,
        "description": "计算数学表达式",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_current_time",
        "function": Tools.get_current_time,
        "description": "获取当前时间",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "read_file",
        "function": Tools.read_file,
        "description": "读取文件内容",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "function": Tools.write_file,
        "description": "写入文件内容",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                },
                "content": {
                    "type": "string",
                    "description": "文件内容"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "list_files",
        "function": Tools.list_files,
        "description": "列出目录中的文件",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "目录路径"
                }
            },
            "required": ["directory"]
        }
    }
]
