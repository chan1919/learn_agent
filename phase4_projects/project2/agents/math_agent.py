from agents.base_agent import BaseAgent
from tools import tools
import re

class MathAgent(BaseAgent):
    """
    数学计算 Agent
    """
    
    def __init__(self):
        """
        初始化数学计算 Agent
        """
        super().__init__("MathAgent", "数学计算 Agent，负责执行数学计算任务")
    
    def process_task(self, task: str) -> str:
        """
        处理数学计算任务
        
        Args:
            task: 任务描述
            
        Returns:
            数学计算结果
        """
        try:
            self.logger.info(f"处理数学计算任务: {task}")
            
            # 添加上下文
            self.add_context("user", task)
            
            # 提取数学表达式
            expression = self._extract_expression(task)
            self.logger.info(f"提取到表达式: {expression}")
            
            # 执行计算
            result = tools.calculate(expression)
            self.logger.info(f"计算结果: {result}")
            
            # 添加上下文
            self.add_context("assistant", result)
            
            return result
            
        except Exception as e:
            error_msg = f"处理数学计算任务时出错: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def _extract_expression(self, task: str) -> str:
        """
        提取数学表达式
        
        Args:
            task: 任务描述
            
        Returns:
            数学表达式
        """
        # 简单的表达式提取，实际项目中应使用更复杂的 NLP 技术
        match = re.search(r"(?:计算|等于)[:：]?\s*([^\s]+)", task)
        if match:
            return match.group(1)
        
        # 尝试直接提取数字和运算符
        match = re.search(r"([\d\+\-\*\/\(\)\.]+)", task)
        if match:
            return match.group(1)
        
        return "0"  # 默认表达式
