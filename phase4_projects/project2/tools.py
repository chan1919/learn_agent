import requests
import os
from datetime import datetime

class Tools:
    """工具类，提供各种功能"""
    
    @staticmethod
    def get_weather(city: str) -> str:
        """
        查询天气信息
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息字符串
        """
        try:
            # 这里使用模拟数据，实际项目中应调用真实的天气 API
            weather_data = {
                "北京": "晴，温度 15-25°C，风力 3-4 级",
                "上海": "多云，温度 18-28°C，风力 2-3 级",
                "广州": "阴，温度 22-30°C，风力 1-2 级",
                "深圳": "小雨，温度 20-26°C，风力 2-3 级"
            }
            
            if city in weather_data:
                return f"{city}的天气：{weather_data[city]}"
            else:
                return f"抱歉，暂不支持查询{city}的天气信息"
        except Exception as e:
            return f"查询天气时出错：{str(e)}"
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容字符串
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"文件内容：\n{content}"
            else:
                return f"文件不存在：{file_path}"
        except Exception as e:
            return f"读取文件时出错：{str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            
        Returns:
            操作结果字符串
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"文件写入成功：{file_path}"
        except Exception as e:
            return f"写入文件时出错：{str(e)}"
    
    @staticmethod
    def get_current_time() -> str:
        """
        获取当前时间
        
        Returns:
            当前时间字符串
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"当前时间：{current_time}"
        except Exception as e:
            return f"获取时间时出错：{str(e)}"
    
    @staticmethod
    def calculate(expression: str) -> str:
        """
        计算数学表达式
        
        Args:
            expression: 数学表达式
            
        Returns:
            计算结果字符串
        """
        try:
            # 简单的数学计算，实际项目中应使用更安全的计算方法
            result = eval(expression)
            return f"计算结果：{result}"
        except Exception as e:
            return f"计算时出错：{str(e)}"

# 创建工具实例
tools = Tools()
