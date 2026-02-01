from config import config
from tools import tools
import logging
import time

# 配置日志
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class SmartAssistantAgent:
    """智能助手 Agent 类"""
    
    def __init__(self):
        """初始化 Agent"""
        self.tools = tools
        self.context = []
        self.tool_calls = 0
        logger.info("SmartAssistantAgent 初始化完成")
    
    def execute_task(self, task: str) -> str:
        """
        执行任务
        
        Args:
            task: 任务描述
            
        Returns:
            任务执行结果
        """
        try:
            logger.info(f"开始执行任务: {task}")
            
            # 添加任务到上下文
            self.context.append({"role": "user", "content": task})
            
            # 分析任务
            task_type = self._analyze_task(task)
            logger.info(f"任务类型: {task_type}")
            
            # 执行任务
            if task_type == "weather":
                # 提取城市名称
                city = self._extract_city(task)
                result = self.tools.get_weather(city)
            elif task_type == "file_read":
                # 提取文件路径
                file_path = self._extract_file_path(task)
                result = self.tools.read_file(file_path)
            elif task_type == "file_write":
                # 提取文件路径和内容
                file_path, content = self._extract_file_write_info(task)
                result = self.tools.write_file(file_path, content)
            elif task_type == "time":
                result = self.tools.get_current_time()
            elif task_type == "calculation":
                # 提取数学表达式
                expression = self._extract_expression(task)
                result = self.tools.calculate(expression)
            else:
                # 通用任务处理
                result = self._handle_generic_task(task)
            
            # 添加结果到上下文
            self.context.append({"role": "assistant", "content": result})
            
            logger.info(f"任务执行完成: {result}")
            return result
            
        except Exception as e:
            error_msg = f"执行任务时出错: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _analyze_task(self, task: str) -> str:
        """
        分析任务类型
        
        Args:
            task: 任务描述
            
        Returns:
            任务类型
        """
        task = task.lower()
        
        if any(keyword in task for keyword in ["天气", "气温", "温度"]):
            return "weather"
        elif any(keyword in task for keyword in ["读", "查看", "读取", "打开"]):
            return "file_read"
        elif any(keyword in task for keyword in ["写", "保存", "写入", "创建"]):
            return "file_write"
        elif any(keyword in task for keyword in ["时间", "几点", "现在"]):
            return "time"
        elif any(keyword in task for keyword in ["计算", "等于", "加", "减", "乘", "除"]):
            return "calculation"
        else:
            return "generic"
    
    def _extract_city(self, task: str) -> str:
        """
        提取城市名称
        
        Args:
            task: 任务描述
            
        Returns:
            城市名称
        """
        # 简单的城市名称提取，实际项目中应使用更复杂的 NLP 技术
        cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "西安"]
        for city in cities:
            if city in task:
                return city
        return "北京"  # 默认城市
    
    def _extract_file_path(self, task: str) -> str:
        """
        提取文件路径
        
        Args:
            task: 任务描述
            
        Returns:
            文件路径
        """
        # 简单的文件路径提取，实际项目中应使用更复杂的 NLP 技术
        import re
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
        
        import re
        # 提取文件路径
        path_match = re.search(r"(?:文件|路径|保存|写入|创建)[:：]?\s*([^\s]+)", task)
        if path_match:
            file_path = path_match.group(1)
        
        # 提取内容
        content_match = re.search(r"(?:内容|写入|保存)[:：]?\s*(.+)", task)
        if content_match:
            content = content_match.group(1)
        
        return file_path, content
    
    def _extract_expression(self, task: str) -> str:
        """
        提取数学表达式
        
        Args:
            task: 任务描述
            
        Returns:
            数学表达式
        """
        # 简单的表达式提取，实际项目中应使用更复杂的 NLP 技术
        import re
        match = re.search(r"(?:计算|等于)[:：]?\s*([^\s]+)", task)
        if match:
            return match.group(1)
        
        # 尝试直接提取数字和运算符
        match = re.search(r"([\d\+\-\*\/\(\)\.]+)", task)
        if match:
            return match.group(1)
        
        return "0"  # 默认表达式
    
    def _handle_generic_task(self, task: str) -> str:
        """
        处理通用任务
        
        Args:
            task: 任务描述
            
        Returns:
            任务处理结果
        """
        # 这里使用简单的响应，实际项目中应调用大语言模型生成响应
        return f"我已收到您的任务: {task}\n这是一个通用任务，我会尽快处理。"
    
    def clear_context(self):
        """
        清空上下文
        """
        self.context = []
        logger.info("上下文已清空")
    
    def get_context(self) -> list:
        """
        获取上下文
        
        Returns:
            上下文列表
        """
        return self.context

# 创建全局 Agent 实例
global_agent = SmartAssistantAgent()
