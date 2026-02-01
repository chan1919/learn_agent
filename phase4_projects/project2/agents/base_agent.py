import logging
from abc import ABC, abstractmethod
from config import config

class BaseAgent(ABC):
    """
    基础 Agent 类，所有 Agent 的基类
    """
    
    def __init__(self, name: str, description: str):
        """
        初始化 Agent
        
        Args:
            name: Agent 名称
            description: Agent 描述
        """
        self.name = name
        self.description = description
        self.context = []
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        self.logger.info(f"初始化 Agent: {name}")
    
    @abstractmethod
    def process_task(self, task: str) -> str:
        """
        处理任务
        
        Args:
            task: 任务描述
            
        Returns:
            任务处理结果
        """
        pass
    
    def add_context(self, role: str, content: str):
        """
        添加上下文
        
        Args:
            role: 角色
            content: 内容
        """
        self.context.append({"role": role, "content": content})
    
    def get_context(self) -> list:
        """
        获取上下文
        
        Returns:
            上下文列表
        """
        return self.context
    
    def clear_context(self):
        """
        清空上下文
        """
        self.context = []
    
    def get_info(self) -> dict:
        """
        获取 Agent 信息
        
        Returns:
            Agent 信息字典
        """
        return {
            "name": self.name,
            "description": self.description
        }
