"""
基于大语言模型的Agent实现
"""

import os
import json
from typing import Dict, List, Optional, Any


class LLMAgent:
    """
    基于大语言模型的Agent类
    用于处理复杂的自然语言任务，具备推理、规划和执行能力
    """
    
    def __init__(self, model_name: str = "gpt-4", api_key: Optional[str] = None):
        """
        初始化LLMAgent
        
        Args:
            model_name: 使用的大语言模型名称
            api_key: API密钥，如果为None则从环境变量获取
        """
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.memory = []  # 存储对话历史
        self.tools = {}  # 可用工具
        
    def add_tool(self, tool_name: str, tool_func, description: str):
        """
        添加工具到Agent
        
        Args:
            tool_name: 工具名称
            tool_func: 工具函数
            description: 工具描述
        """
        self.tools[tool_name] = {
            "function": tool_func,
            "description": description
        }
    
    def process(self, prompt: str) -> str:
        """
        处理用户输入
        
        Args:
            prompt: 用户输入
            
        Returns:
            Agent的响应
        """
        # 存储用户输入到记忆
        self.memory.append({"role": "user", "content": prompt})
        
        # 构建完整的提示
        full_prompt = self._build_prompt()
        
        # 这里应该调用实际的LLM API，现在返回模拟响应
        response = self._mock_llm_response(full_prompt)
        
        # 存储Agent响应到记忆
        self.memory.append({"role": "assistant", "content": response})
        
        return response
    
    def _build_prompt(self) -> str:
        """
        构建完整的提示
        
        Returns:
            完整的提示字符串
        """
        prompt = "你是一个智能助手，能够帮助用户完成各种任务。\n"
        
        # 添加工具信息
        if self.tools:
            prompt += "\n可用工具：\n"
            for tool_name, tool_info in self.tools.items():
                prompt += f"- {tool_name}: {tool_info['description']}\n"
        
        # 添加对话历史
        prompt += "\n对话历史：\n"
        for message in self.memory:
            prompt += f"{message['role']}: {message['content']}\n"
        
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
        return f"基于你的输入，我需要思考如何回应...\n提示长度: {len(prompt)} 字符\n可用工具数量: {len(self.tools)}"
    
    def clear_memory(self):
        """
        清空对话记忆
        """
        self.memory = []


class AutonomousAgent:
    """
    自主Agent系统
    具备自我规划、执行和反思能力
    """
    
    def __init__(self, name: str, goal: str, llm_agent: LLMAgent):
        """
        初始化自主Agent
        
        Args:
            name: Agent名称
            goal: Agent目标
            llm_agent: 底层LLM Agent
        """
        self.name = name
        self.goal = goal
        self.llm_agent = llm_agent
        self.plan = []  # 行动计划
        self.execution_history = []  # 执行历史
        
    def set_goal(self, goal: str):
        """
        设置Agent目标
        
        Args:
            goal: 新的目标
        """
        self.goal = goal
        self.plan = []  # 重置计划
        
    def generate_plan(self) -> List[str]:
        """
        生成行动计划
        
        Returns:
            行动计划列表
        """
        prompt = f"基于目标 '{self.goal}'，生成一个详细的行动计划，包含具体的步骤。"
        response = self.llm_agent.process(prompt)
        
        # 解析响应生成计划（实际应用中需要更复杂的解析）
        self.plan = [f"步骤 {i+1}: {step}" for i, step in enumerate(response.split('\n')[:3])]
        
        return self.plan
    
    def execute_plan(self):
        """
        执行行动计划
        """
        if not self.plan:
            self.generate_plan()
        
        for step in self.plan:
            print(f"执行: {step}")
            # 执行步骤（实际应用中需要更复杂的执行逻辑）
            self.execution_history.append({"step": step, "status": "completed"})
            
    def reflect(self):
        """
        反思执行过程
        
        Returns:
            反思结果
        """
        prompt = f"基于执行历史 {self.execution_history}，反思执行过程中的成功和失败，并提出改进建议。"
        return self.llm_agent.process(prompt)