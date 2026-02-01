"""
记忆管理模块
"""

from typing import Dict, List, Any, Optional
from config import MAX_MEMORY_SIZE


class MemoryManager:
    """
    记忆管理器
    用于管理智能助手的对话记忆
    """
    
    def __init__(self, max_size: int = MAX_MEMORY_SIZE):
        """
        初始化记忆管理器
        
        Args:
            max_size: 最大记忆大小
        """
        self.max_size = max_size
        self.memory = []  # 记忆列表
        self.user_preferences = {}  # 用户偏好
    
    def add_memory(self, memory: Dict[str, Any]):
        """
        添加记忆
        
        Args:
            memory: 记忆内容，格式为 {"role": 角色, "content": 内容}
        """
        self.memory.append(memory)
        
        # 保持记忆大小不超过最大值
        if len(self.memory) > self.max_size:
            self.memory = self.memory[-self.max_size:]
    
    def get_memory(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取记忆
        
        Args:
            limit: 返回的记忆数量限制，如果为None则返回所有记忆
            
        Returns:
            记忆列表
        """
        if limit:
            return self.memory[-limit:]
        return self.memory
    
    def clear_memory(self):
        """
        清空记忆
        """
        self.memory = []
    
    def set_preference(self, key: str, value: Any):
        """
        设置用户偏好
        
        Args:
            key: 偏好键
            value: 偏好值
        """
        self.user_preferences[key] = value
    
    def get_preference(self, key: str) -> Optional[Any]:
        """
        获取用户偏好
        
        Args:
            key: 偏好键
            
        Returns:
            偏好值，如果不存在返回None
        """
        return self.user_preferences.get(key)
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """
        获取所有用户偏好
        
        Returns:
            用户偏好字典
        """
        return self.user_preferences
