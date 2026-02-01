from agents.base_agent import BaseAgent
from tools import tools

class WeatherAgent(BaseAgent):
    """
    天气查询 Agent
    """
    
    def __init__(self):
        """
        初始化天气查询 Agent
        """
        super().__init__("WeatherAgent", "天气查询 Agent，负责查询城市天气信息")
    
    def process_task(self, task: str) -> str:
        """
        处理天气查询任务
        
        Args:
            task: 任务描述
            
        Returns:
            天气查询结果
        """
        try:
            self.logger.info(f"处理天气查询任务: {task}")
            
            # 添加上下文
            self.add_context("user", task)
            
            # 提取城市名称
            city = self._extract_city(task)
            self.logger.info(f"提取到城市: {city}")
            
            # 查询天气
            result = tools.get_weather(city)
            self.logger.info(f"天气查询结果: {result}")
            
            # 添加上下文
            self.add_context("assistant", result)
            
            return result
            
        except Exception as e:
            error_msg = f"处理天气查询任务时出错: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
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
