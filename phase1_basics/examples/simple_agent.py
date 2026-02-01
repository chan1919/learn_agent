# 简单的反应式 Agent 示例
# 温度调节 Agent

class TemperatureAgent:
    """
    一个简单的反应式温度调节 Agent
    能够感知环境温度并做出相应的调节动作
    """

    def __init__(self, target_temperature=22):
        """
        初始化温度调节 Agent

        参数:
            target_temperature: 目标温度，默认为 22 摄氏度
        """
        self.target_temperature = target_temperature
        self.min_temperature = 18  # 最低温度
        self.max_temperature = 26  # 最高温度
        self.status = "idle"  # 初始状态为空闲

    def perceive(self, current_temperature):
        """
        感知环境温度

        参数:
            current_temperature: 当前环境温度

        返回:
            感知到的温度值
        """
        print(f"感知到当前温度: {current_temperature}°C")
        return current_temperature

    def decide(self, current_temperature):
        """
        根据感知到的温度做出决策

        参数:
            current_temperature: 当前环境温度

        返回:
            决策结果，即需要执行的动作
        """
        if current_temperature < self.target_temperature - 1:
            # 温度低于目标温度 1 度以上，需要加热
            action = "heat"
            self.status = "heating"
        elif current_temperature > self.target_temperature + 1:
            # 温度高于目标温度 1 度以上，需要制冷
            action = "cool"
            self.status = "cooling"
        else:
            # 温度在目标温度附近，不需要调节
            action = "idle"
            self.status = "idle"

        print(f"决策结果: {action}")
        return action

    def act(self, action):
        """
        执行决策结果，调节温度

        参数:
            action: 需要执行的动作

        返回:
            执行结果
        """
        if action == "heat":
            result = "正在加热..."
        elif action == "cool":
            result = "正在制冷..."
        else:
            result = "温度适宜，无需调节"

        print(f"执行动作: {result}")
        return result

    def run(self, current_temperature):
        """
        运行 Agent 的完整循环：感知-决策-行动

        参数:
            current_temperature: 当前环境温度

        返回:
            执行结果
        """
        # 1. 感知环境
        perceived_temp = self.perceive(current_temperature)

        # 2. 做出决策
        action = self.decide(perceived_temp)

        # 3. 执行动作
        result = self.act(action)

        # 4. 返回执行结果
        return result

    def get_status(self):
        """
        获取 Agent 当前状态

        返回:
            当前状态
        """
        return self.status


# 测试代码
if __name__ == "__main__":
    print("=== 温度调节 Agent 测试 ===")

    # 创建温度调节 Agent 实例，目标温度设为 22 度
    agent = TemperatureAgent(target_temperature=22)

    # 测试不同温度场景
    test_temperatures = [15, 20, 22, 24, 28]

    for temp in test_temperatures:
        print(f"\n--- 测试温度: {temp}°C ---")
        result = agent.run(temp)
        print(f"当前状态: {agent.get_status()}")

    print("\n=== 测试完成 ===")
