import unittest
from agent import SmartAssistantAgent

class TestSmartAssistantAgent(unittest.TestCase):
    """
    测试 SmartAssistantAgent 类
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        self.agent = SmartAssistantAgent()
    
    def test_weather_task(self):
        """
        测试天气查询任务
        """
        result = self.agent.execute_task("北京的天气如何")
        self.assertIn("北京的天气", result)
    
    def test_time_task(self):
        """
        测试时间查询任务
        """
        result = self.agent.execute_task("现在几点了")
        self.assertIn("当前时间", result)
    
    def test_calculation_task(self):
        """
        测试数学计算任务
        """
        result = self.agent.execute_task("计算 1+2*3")
        self.assertIn("计算结果", result)
    
    def test_generic_task(self):
        """
        测试通用任务
        """
        result = self.agent.execute_task("你好，今天过得怎么样")
        self.assertIn("我已收到您的任务", result)
    
    def test_clear_context(self):
        """
        测试清空上下文
        """
        # 先执行一个任务
        self.agent.execute_task("北京的天气如何")
        # 检查上下文长度
        self.assertGreater(len(self.agent.get_context()), 0)
        # 清空上下文
        self.agent.clear_context()
        # 检查上下文是否为空
        self.assertEqual(len(self.agent.get_context()), 0)

if __name__ == "__main__":
    unittest.main()
