# 基础 Agent 交互流程示例
# 智能家居多 Agent 系统

class BaseAgent:
    """
    基础 Agent 类，定义了所有 Agent 共有的属性和方法
    """
    
    def __init__(self, name, agent_type):
        """
        初始化基础 Agent
        
        参数:
            name: Agent 的名称
            agent_type: Agent 的类型
        """
        self.name = name
        self.agent_type = agent_type
        self.status = "idle"
        self.messages = []
    
    def receive_message(self, sender, message):
        """
        接收来自其他 Agent 的消息
        
        参数:
            sender: 消息发送者
            message: 消息内容
        """
        self.messages.append((sender, message))
        print(f"[{self.name}] 收到来自 {sender} 的消息: {message}")
    
    def send_message(self, receiver, message):
        """
        向其他 Agent 发送消息
        
        参数:
            receiver: 消息接收者
            message: 消息内容
        """
        print(f"[{self.name}] 发送消息给 {receiver.name}: {message}")
        receiver.receive_message(self.name, message)
    
    def get_status(self):
        """
        获取 Agent 当前状态
        
        返回:
            当前状态
        """
        return self.status
    
    def set_status(self, status):
        """
        设置 Agent 状态
        
        参数:
            status: 新的状态
        """
        self.status = status
        print(f"[{self.name}] 状态变更为: {status}")


class TemperatureAgent(BaseAgent):
    """
    温度监控和调节 Agent
    """
    
    def __init__(self, name="温度 Agent"):
        """
        初始化温度 Agent
        
        参数:
            name: Agent 的名称
        """
        super().__init__(name, "temperature")
        self.current_temperature = 22
        self.target_temperature = 22
    
    def monitor_temperature(self):
        """
        监控当前温度
        
        返回:
            当前温度
        """
        print(f"[{self.name}] 监控到当前温度: {self.current_temperature}°C")
        return self.current_temperature
    
    def adjust_temperature(self, action):
        """
        调节温度
        
        参数:
            action: 调节动作 (heat/cool/idle)
        """
        if action == "heat":
            self.current_temperature += 1
            self.set_status("heating")
        elif action == "cool":
            self.current_temperature -= 1
            self.set_status("cooling")
        else:
            self.set_status("idle")
        
        print(f"[{self.name}] 温度调节后: {self.current_temperature}°C")
    
    def run(self):
        """
        运行温度 Agent
        """
        temp = self.monitor_temperature()
        
        if temp < self.target_temperature - 1:
            return "heat"
        elif temp > self.target_temperature + 1:
            return "cool"
        else:
            return "idle"


class HumidityAgent(BaseAgent):
    """
    湿度监控和调节 Agent
    """
    
    def __init__(self, name="湿度 Agent"):
        """
        初始化湿度 Agent
        
        参数:
            name: Agent 的名称
        """
        super().__init__(name, "humidity")
        self.current_humidity = 45
        self.target_humidity = 45
    
    def monitor_humidity(self):
        """
        监控当前湿度
        
        返回:
            当前湿度
        """
        print(f"[{self.name}] 监控到当前湿度: {self.current_humidity}%")
        return self.current_humidity
    
    def adjust_humidity(self, action):
        """
        调节湿度
        
        参数:
            action: 调节动作 (humidify/dehumidify/idle)
        """
        if action == "humidify":
            self.current_humidity += 2
            self.set_status("humidifying")
        elif action == "dehumidify":
            self.current_humidity -= 2
            self.set_status("dehumidifying")
        else:
            self.set_status("idle")
        
        print(f"[{self.name}] 湿度调节后: {self.current_humidity}%")
    
    def run(self):
        """
        运行湿度 Agent
        """
        humidity = self.monitor_humidity()
        
        if humidity < self.target_humidity - 5:
            return "humidify"
        elif humidity > self.target_humidity + 5:
            return "dehumidify"
        else:
            return "idle"


class MCPCoordinator(BaseAgent):
    """
    主控程序协调器，负责协调多个 Agent 工作
    """
    
    def __init__(self, name="MCP 协调器"):
        """
        初始化 MCP 协调器
        
        参数:
            name: Agent 的名称
        """
        super().__init__(name, "mcp")
        self.agents = []
    
    def register_agent(self, agent):
        """
        注册 Agent 到协调器
        
        参数:
            agent: 要注册的 Agent
        """
        self.agents.append(agent)
        print(f"[{self.name}] 注册了新 Agent: {agent.name}")
    
    def collect_status(self):
        """
        收集所有 Agent 的状态
        
        返回:
            状态字典
        """
        status_dict = {}
        for agent in self.agents:
            status_dict[agent.name] = agent.get_status()
        
        print(f"[{self.name}] 收集到的状态: {status_dict}")
        return status_dict
    
    def coordinate(self):
        """
        协调多个 Agent 工作
        """
        print(f"\n[{self.name}] 开始协调工作...")
        
        # 收集所有 Agent 的运行结果
        actions = {}
        for agent in self.agents:
            if hasattr(agent, "run"):
                action = agent.run()
                actions[agent.name] = action
                print(f"[{self.name}] {agent.name} 需要执行: {action}")
        
        # 执行调节动作
        for agent in self.agents:
            if agent.name in actions:
                if hasattr(agent, "adjust_temperature"):
                    agent.adjust_temperature(actions[agent.name])
                elif hasattr(agent, "adjust_humidity"):
                    agent.adjust_humidity(actions[agent.name])
        
        # 发送协调结果
        for agent in self.agents:
            self.send_message(agent, f"协调完成，当前系统状态正常")
        
        print(f"[{self.name}] 协调工作完成")


# 测试代码
if __name__ == "__main__":
    print("=== 智能家居多 Agent 系统测试 ===")
    
    # 创建各个 Agent
    mcp = MCPCoordinator()
    temp_agent = TemperatureAgent()
    humidity_agent = HumidityAgent()
    
    # 注册 Agent 到 MCP
    mcp.register_agent(temp_agent)
    mcp.register_agent(humidity_agent)
    
    # 模拟温度和湿度变化
    print("\n--- 模拟温度变化: 降低到 19°C ---")
    temp_agent.current_temperature = 19
    
    print("\n--- 模拟湿度变化: 升高到 55% ---")
    humidity_agent.current_humidity = 55
    
    # MCP 协调工作
    mcp.coordinate()
    
    # 再次运行协调
    print("\n--- 再次运行协调 ---")
    mcp.coordinate()
    
    # 测试 Agent 之间的直接通信
    print("\n--- 测试 Agent 之间的直接通信 ---")
    temp_agent.send_message(humidity_agent, "温度已调节到适宜范围")
    humidity_agent.send_message(temp_agent, "湿度调节中，请稍候")
    
    # 收集最终状态
    print("\n--- 收集最终系统状态 ---")
    mcp.collect_status()
    
    print("\n=== 测试完成 ===")
