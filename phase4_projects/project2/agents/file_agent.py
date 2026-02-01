from agents.base_agent import BaseAgent
from tools import tools
import re

class FileAgent(BaseAgent):
    """
    文件操作 Agent
    """
    
    def __init__(self):
        """
        初始化文件操作 Agent
        """
        super().__init__("FileAgent", "文件操作 Agent，负责文件读取和写入操作")
    
    def process_task(self, task: str) -> str:
        """
        处理文件操作任务
        
        Args:
            task: 任务描述
            
        Returns:
            文件操作结果
        """
        try:
            self.logger.info(f"处理文件操作任务: {task}")
            
            # 添加上下文
            self.add_context("user", task)
            
            # 分析任务类型
            task_type = self._analyze_task_type(task)
            self.logger.info(f"文件操作类型: {task_type}")
            
            # 执行相应操作
            if task_type == "read":
                # 提取文件路径
                file_path = self._extract_file_path(task)
                result = tools.read_file(file_path)
            elif task_type == "write":
                # 提取文件路径和内容
                file_path, content = self._extract_file_write_info(task)
                result = tools.write_file(file_path, content)
            else:
                result = "不支持的文件操作类型"
            
            self.logger.info(f"文件操作结果: {result}")
            
            # 添加上下文
            self.add_context("assistant", result)
            
            return result
            
        except Exception as e:
            error_msg = f"处理文件操作任务时出错: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def _analyze_task_type(self, task: str) -> str:
        """
        分析文件操作类型
        
        Args:
            task: 任务描述
            
        Returns:
            任务类型
        """
        task = task.lower()
        
        if any(keyword in task for keyword in ["读", "查看", "读取", "打开"]):
            return "read"
        elif any(keyword in task for keyword in ["写", "保存", "写入", "创建"]):
            return "write"
        else:
            return "unknown"
    
    def _extract_file_path(self, task: str) -> str:
        """
        提取文件路径
        
        Args:
            task: 任务描述
            
        Returns:
            文件路径
        """
        # 简单的文件路径提取，实际项目中应使用更复杂的 NLP 技术
        match = re.search(r"(?:文件|路径|打开|查看|读取)[:：]?\s*([^\s]+)", task)
        if match:
            return match.group(1)
        return "example.txt"  # 默认文件路径
    
    def _extract_file_write_info(self, task: str) -> tuple:
        """
        提取文件写入信息
        
        Args:
            task: 任务描述
            
        Returns:
            (文件路径, 内容) 元组
        """
        # 简单的信息提取，实际项目中应使用更复杂的 NLP 技术
        file_path = "output.txt"  # 默认文件路径
        content = "Hello, World!"  # 默认内容
        
        # 提取文件路径
        path_match = re.search(r"(?:文件|路径|保存|写入|创建)[:：]?\s*([^\s]+)", task)
        if path_match:
            file_path = path_match.group(1)
        
        # 提取内容
        content_match = re.search(r"(?:内容|写入|保存)[:：]?\s*(.+)", task)
        if content_match:
            content = content_match.group(1)
        
        return file_path, content
