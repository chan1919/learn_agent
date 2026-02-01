import unittest
from mcp import MasterControlProgram

class TestMasterControlProgram(unittest.TestCase):
    """
    测试 MasterControlProgram 类
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        self.mcp = MasterControlProgram()
    
    def test_weather_task(self):
        """
        测试天气查询任务
        """
        result = self.mcp.submit_task("北京的天气如何")
        self.assertIn("北京的天气", result)
    
    def test_math_task(self):
        """
        测试数学计算任务
        """
        result = self.mcp.submit_task("计算 1+2*3")
        self.assertIn("计算结果", result)
    
    def test_complex_task(self):
        """
        测试复杂任务（多个子任务）
        """
        result = self.mcp.submit_task("查询北京的天气并计算 1+2*3")
        self.assertIn("北京的天气", result)
        self.assertIn("计算结果", result)
    
    def test_get_agents_info(self):
        """
        测试获取 Agent 信息
        """
        agents_info = self.mcp.get_agents_info()
        self.assertIn("weather", agents_info)
        self.assertIn("file", agents_info)
        self.assertIn("math", agents_info)
    
    def test_history(self):
        """
        测试历史任务
        """
        # 提交任务
        self.mcp.submit_task("北京的天气如何")
        # 检查历史任务
        history = self.mcp.get_history()
        self.assertGreater(len(history), 0)
        # 清空历史任务
        self.mcp.clear_history()
        # 检查历史任务是否为空
        history = self.mcp.get_history()
        self.assertEqual(len(history), 0)

if __name__ == "__main__":
    unittest.main()
