"""
智能助手应用场景
"""

from typing import Dict, List, Optional, Any
from phase3_advanced.advanced_agents.llm_agent import LLMAgent


class SmartAssistant:
    """
    智能助手
    基于大语言模型，具备多轮对话、工具使用、个性化服务能力
    """
    
    def __init__(self, name: str = "智能助手"):
        """
        初始化智能助手
        
        Args:
            name: 助手名称
        """
        self.name = name
        self.llm_agent = LLMAgent()
        self.user_preferences = {}  # 用户偏好设置
        
        # 注册内置工具
        self._register_builtin_tools()
    
    def chat(self, message: str) -> str:
        """
        与用户对话
        
        Args:
            message: 用户输入
            
        Returns:
            助手的响应
        """
        # 处理用户输入
        response = self.llm_agent.process(message)
        
        return response
    
    def set_preference(self, key: str, value: Any):
        """
        设置用户偏好
        
        Args:
            key: 偏好键
            value: 偏好值
        """
        self.user_preferences[key] = value
        print(f"已设置偏好: {key} = {value}")
    
    def get_preference(self, key: str) -> Optional[Any]:
        """
        获取用户偏好
        
        Args:
            key: 偏好键
            
        Returns:
            偏好值，如果不存在返回None
        """
        return self.user_preferences.get(key)
    
    def _register_builtin_tools(self):
        """
        注册内置工具
        """
        # 注册天气查询工具
        def get_weather(city: str) -> str:
            """获取城市天气"""
            # 模拟天气查询
            return f"{city}的天气晴朗，温度25℃"
        
        self.llm_agent.add_tool("get_weather", get_weather, "获取指定城市的天气信息")
        
        # 注册计算器工具
        def calculate(expression: str) -> str:
            """计算数学表达式"""
            try:
                result = eval(expression)
                return f"计算结果: {result}"
            except Exception as e:
                return f"计算错误: {str(e)}"
        
        self.llm_agent.add_tool("calculate", calculate, "计算数学表达式")
        
        # 注册时间查询工具
        def get_current_time() -> str:
            """获取当前时间"""
            import time
            return f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.llm_agent.add_tool("get_current_time", get_current_time, "获取当前时间")
    
    def add_custom_tool(self, tool_name: str, tool_func, description: str):
        """
        添加自定义工具
        
        Args:
            tool_name: 工具名称
            tool_func: 工具函数
            description: 工具描述
        """
        self.llm_agent.add_tool(tool_name, tool_func, description)
        print(f"已添加自定义工具: {tool_name}")
