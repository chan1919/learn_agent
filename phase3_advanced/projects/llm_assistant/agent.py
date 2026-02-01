"""
智能助手核心
"""

from typing import Dict, List, Any, Optional
from config import OPENAI_API_KEY, MODEL_NAME, AGENT_NAME, TEMPERATURE, MAX_TOKENS
from memory import MemoryManager
from tools import tool_list


class LLMAssistant:
    """
    基于LLM的智能助手
    """
    
    def __init__(self):
        """
        初始化智能助手
        """
        self.name = AGENT_NAME
        self.memory_manager = MemoryManager()
        self.tools = {tool["name"]: tool for tool in tool_list}
        
    def chat(self, message: str) -> str:
        """
        与用户对话
        
        Args:
            message: 用户输入
            
        Returns:
            助手的响应
        """
        # 添加用户输入到记忆
        self.memory_manager.add_memory({"role": "user", "content": message})
        
        # 构建完整的提示
        prompt = self._build_prompt()
        
        # 这里应该调用实际的LLM API，现在返回模拟响应
        response = self._mock_llm_response(prompt)
        
        # 检查是否需要使用工具
        tool_call = self._parse_tool_call(response)
        if tool_call:
            # 执行工具
            tool_result = self._execute_tool(tool_call)
            
            # 将工具执行结果添加到记忆
            self.memory_manager.add_memory({"role": "assistant", "content": f"执行工具: {tool_call['name']}, 结果: {tool_result}"})
            
            # 再次构建提示，包含工具执行结果
            prompt = self._build_prompt()
            response = self._mock_llm_response(prompt)
        
        # 添加助手响应到记忆
        self.memory_manager.add_memory({"role": "assistant", "content": response})
        
        return response
    
    def _build_prompt(self) -> str:
        """
        构建完整的提示
        
        Returns:
            完整的提示字符串
        """
        prompt = f"你是{self.name}，一个智能助手，能够帮助用户完成各种任务。\n"
        
        # 添加工具信息
        if self.tools:
            prompt += "\n可用工具：\n"
            for tool_name, tool_info in self.tools.items():
                prompt += f"- {tool_name}: {tool_info['description']}\n"
        
        # 添加用户偏好
        preferences = self.memory_manager.get_all_preferences()
        if preferences:
            prompt += "\n用户偏好：\n"
            for key, value in preferences.items():
                prompt += f"- {key}: {value}\n"
        
        # 添加对话历史
        memory = self.memory_manager.get_memory()
        if memory:
            prompt += "\n对话历史：\n"
            for item in memory:
                prompt += f"{item['role']}: {item['content']}\n"
        
        return prompt
    
    def _mock_llm_response(self, prompt: str) -> str:
        """
        模拟LLM响应
        
        Args:
            prompt: 完整的提示
            
        Returns:
            模拟的响应
        """
        # 简单的模拟响应，实际应用中应该调用真实的LLM API
        if "天气" in prompt:
            return "请问您想查询哪个城市的天气？"
        elif "计算" in prompt or "等于" in prompt:
            return "我可以帮您计算，请提供数学表达式。"
        elif "时间" in prompt:
            return "现在是 2026年2月1日 22:00:00"
        elif "文件" in prompt:
            return "我可以帮您操作文件，请提供具体的文件路径和操作。"
        else:
            return "我是智能助手，很高兴为您服务！"
    
    def _parse_tool_call(self, response: str) -> Optional[Dict[str, Any]]:
        """
        解析工具调用
        
        Args:
            response: LLM的响应
            
        Returns:
            工具调用信息，如果不是工具调用返回None
        """
        # 简单的解析，实际应用中应该使用更复杂的解析
        return None
    
    def _execute_tool(self, tool_call: Dict[str, Any]) -> str:
        """
        执行工具
        
        Args:
            tool_call: 工具调用信息
            
        Returns:
            工具执行结果
        """
        tool_name = tool_call["name"]
        arguments = tool_call.get("arguments", {})
        
        if tool_name in self.tools:
            tool_func = self.tools[tool_name]["function"]
            try:
                result = tool_func(**arguments)
                return result
            except Exception as e:
                return f"工具执行错误: {str(e)}"
        else:
            return f"工具不存在: {tool_name}"
    
    def set_preference(self, key: str, value: Any):
        """
        设置用户偏好
        
        Args:
            key: 偏好键
            value: 偏好值
        """
        self.memory_manager.set_preference(key, value)
    
    def clear_memory(self):
        """
        清空记忆
        """
        self.memory_manager.clear_memory()
