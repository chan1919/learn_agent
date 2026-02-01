import logging
from config import config
from agents.weather_agent import WeatherAgent
from agents.file_agent import FileAgent
from agents.math_agent import MathAgent

class MasterControlProgram:
    """
    主控程序，负责任务分配、Agent 管理和协作协调
    """
    
    def __init__(self):
        """
        初始化主控程序
        """
        self.logger = logging.getLogger("MCP")
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # 初始化 Agent 列表
        self.agents = {
            "weather": WeatherAgent(),
            "file": FileAgent(),
            "math": MathAgent()
        }
        
        self.tasks = []
        self.results = []
        
        self.logger.info("MasterControlProgram 初始化完成")
        self.logger.info(f"已注册 {len(self.agents)} 个 Agent")
    
    def submit_task(self, task: str) -> str:
        """
        提交任务
        
        Args:
            task: 任务描述
            
        Returns:
            任务执行结果
        """
        try:
            self.logger.info(f"提交任务: {task}")
            
            # 分析任务
            sub_tasks = self._analyze_task(task)
            self.logger.info(f"任务分析结果: {sub_tasks}")
            
            # 执行子任务
            results = []
            for sub_task_type, sub_task_content in sub_tasks:
                if sub_task_type in self.agents:
                    agent = self.agents[sub_task_type]
                    result = agent.process_task(sub_task_content)
                    results.append(result)
                else:
                    results.append(f"不支持的任务类型: {sub_task_type}")
            
            # 合并结果
            final_result = "\n".join(results)
            self.logger.info(f"任务执行完成: {final_result}")
            
            # 保存任务和结果
            self.tasks.append(task)
            self.results.append(final_result)
            
            return final_result
            
        except Exception as e:
            error_msg = f"执行任务时出错: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def _analyze_task(self, task: str) -> list:
        """
        分析任务，将其分解为子任务
        
        Args:
            task: 任务描述
            
        Returns:
            子任务列表，每个元素为 (任务类型, 任务内容) 元组
        """
        sub_tasks = []
        
        # 检查是否包含天气查询
        if any(keyword in task for keyword in ["天气", "气温", "温度"]):
            sub_tasks.append(("weather", task))
        
        # 检查是否包含文件操作
        if any(keyword in task for keyword in ["文件", "读取", "写入", "保存"]):
            sub_tasks.append(("file", task))
        
        # 检查是否包含数学计算
        if any(keyword in task for keyword in ["计算", "等于", "加", "减", "乘", "除"]):
            sub_tasks.append(("math", task))
        
        # 如果没有识别到任何子任务，返回默认任务
        if not sub_tasks:
            sub_tasks.append(("math", task))  # 临时使用 math agent 处理通用任务
        
        return sub_tasks
    
    def get_agents_info(self) -> dict:
        """
        获取所有 Agent 信息
        
        Returns:
            Agent 信息字典
        """
        agents_info = {}
        for agent_type, agent in self.agents.items():
            agents_info[agent_type] = agent.get_info()
        return agents_info
    
    def clear_history(self):
        """
        清空历史任务和结果
        """
        self.tasks = []
        self.results = []
        self.logger.info("历史任务和结果已清空")
    
    def get_history(self) -> list:
        """
        获取历史任务和结果
        
        Returns:
            历史记录列表
        """
        history = []
        for task, result in zip(self.tasks, self.results):
            history.append({"task": task, "result": result})
        return history
