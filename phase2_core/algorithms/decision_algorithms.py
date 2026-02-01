#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
决策算法实现
"""

from typing import List, Dict, Any, Optional, Callable, Tuple
import random


class DecisionAlgorithm:
    """
    决策算法基类
    """

    def decide(self, state: Any, actions: List[str], **kwargs) -> str:
        """
        从可用动作中选择一个动作

        参数:
            state: 当前状态
            actions: 可用动作列表
            **kwargs: 额外参数

        返回:
            选择的动作
        """
        raise NotImplementedError


class RandomDecision(DecisionAlgorithm):
    """
    随机决策算法
    """

    def decide(self, state: Any, actions: List[str], **kwargs) -> str:
        """
        随机选择一个动作

        参数:
            state: 当前状态
            actions: 可用动作列表
            **kwargs: 额外参数

        返回:
            选择的动作
        """
        if not actions:
            raise ValueError("动作列表不能为空")
        return random.choice(actions)


class GreedyDecision(DecisionAlgorithm):
    """
    贪心决策算法
    """

    def decide(self, state: Any, actions: List[str], evaluation_func: Callable, **kwargs) -> str:
        """
        选择评估值最高的动作

        参数:
            state: 当前状态
            actions: 可用动作列表
            evaluation_func: 评估函数，接收状态和动作，返回评估值
            **kwargs: 额外参数

        返回:
            选择的动作
        """
        if not actions:
            raise ValueError("动作列表不能为空")

        # 评估每个动作
        best_action = actions[0]
        best_value = evaluation_func(state, best_action)

        for action in actions[1:]:
            value = evaluation_func(state, action)
            if value > best_value:
                best_action = action
                best_value = value

        return best_action


class MinimaxDecision(DecisionAlgorithm):
    """
    极小极大决策算法
    """

    def __init__(self, depth: int = 2):
        """
        初始化极小极大决策算法

        参数:
            depth: 搜索深度
        """
        self.depth = depth

    def decide(self, state: Any, actions: List[str], evaluation_func: Callable, transition_func: Callable, is_max_turn: bool = True, **kwargs) -> str:
        """
        使用极小极大算法选择动作

        参数:
            state: 当前状态
            actions: 可用动作列表
            evaluation_func: 评估函数，接收状态，返回评估值
            transition_func: 状态转移函数，接收状态和动作，返回新状态
            is_max_turn: 是否是最大化玩家的回合
            **kwargs: 额外参数

        返回:
            选择的动作
        """
        if not actions:
            raise ValueError("动作列表不能为空")

        best_action = actions[0]
        best_value = float('-inf')

        for action in actions:
            next_state = transition_func(state, action)
            value = self._minimax(next_state, self.depth - 1, not is_max_turn, evaluation_func, transition_func)
            if value > best_value:
                best_action = action
                best_value = value

        return best_action

    def _minimax(self, state: Any, depth: int, is_max_turn: bool, evaluation_func: Callable, transition_func: Callable) -> float:
        """
        极小极大算法的递归实现

        参数:
            state: 当前状态
            depth: 剩余搜索深度
            is_max_turn: 是否是最大化玩家的回合
            evaluation_func: 评估函数
            transition_func: 状态转移函数

        返回:
            状态的评估值
        """
        if depth == 0:
            return evaluation_func(state)

        if is_max_turn:
            max_value = float('-inf')
            # 假设可以获取所有可能的动作
            # 这里简化处理，假设每个状态都有相同的动作列表
            actions = ["action1", "action2", "action3"]  # 实际应用中需要根据状态动态获取
            for action in actions:
                next_state = transition_func(state, action)
                value = self._minimax(next_state, depth - 1, False, evaluation_func, transition_func)
                max_value = max(max_value, value)
            return max_value
        else:
            min_value = float('inf')
            # 假设可以获取所有可能的动作
            actions = ["action1", "action2", "action3"]  # 实际应用中需要根据状态动态获取
            for action in actions:
                next_state = transition_func(state, action)
                value = self._minimax(next_state, depth - 1, True, evaluation_func, transition_func)
                min_value = min(min_value, value)
            return min_value


class QLearningDecision(DecisionAlgorithm):
    """
    Q学习决策算法
    """

    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, exploration_rate: float = 0.1):
        """
        初始化Q学习决策算法

        参数:
            learning_rate: 学习率
            discount_factor: 折扣因子
            exploration_rate: 探索率
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}  # Q表，存储状态-动作对的价值

    def decide(self, state: Any, actions: List[str], **kwargs) -> str:
        """
        根据Q表选择动作

        参数:
            state: 当前状态
            actions: 可用动作列表
            **kwargs: 额外参数

        返回:
            选择的动作
        """
        if not actions:
            raise ValueError("动作列表不能为空")

        # 探索或利用
        if random.random() < self.exploration_rate:
            # 探索：随机选择动作
            return random.choice(actions)
        else:
            # 利用：选择Q值最高的动作
            state_str = str(state)
            if state_str not in self.q_table:
                # 状态不在Q表中，初始化
                self.q_table[state_str] = {action: 0.0 for action in actions}

            # 选择Q值最高的动作
            best_action = actions[0]
            best_value = self.q_table[state_str][best_action]

            for action in actions[1:]:
                value = self.q_table[state_str][action]
                if value > best_value:
                    best_action = action
                    best_value = value

            return best_action

    def learn(self, state: Any, action: str, reward: float, next_state: Any, next_actions: List[str]) -> None:
        """
        更新Q表

        参数:
            state: 当前状态
            action: 执行的动作
            reward: 获得的奖励
            next_state: 下一个状态
            next_actions: 下一个状态的可用动作
        """
        state_str = str(state)
        next_state_str = str(next_state)

        # 确保状态在Q表中
        if state_str not in self.q_table:
            self.q_table[state_str] = {action: 0.0}
        if next_state_str not in self.q_table:
            self.q_table[next_state_str] = {a: 0.0 for a in next_actions}

        # 计算TD目标
        if next_actions:
            max_next_q = max(self.q_table[next_state_str].values())
        else:
            max_next_q = 0.0

        td_target = reward + self.discount_factor * max_next_q

        # 更新Q值
        current_q = self.q_table[state_str].get(action, 0.0)
        new_q = current_q + self.learning_rate * (td_target - current_q)
        self.q_table[state_str][action] = new_q


# 示例使用
def example_usage():
    """
    示例使用
    """
    # 随机决策示例
    print("=== 随机决策示例 ===")
    random_decider = RandomDecision()
    action = random_decider.decide(None, ["前进", "后退", "左转", "右转"])
    print(f"随机选择的动作: {action}")

    # 贪心决策示例
    print("\n=== 贪心决策示例 ===")
    def evaluation_func(state, action):
        """
        简单的评估函数
        """
        scores = {
            "前进": 10,
            "后退": 1,
            "左转": 5,
            "右转": 5
        }
        return scores.get(action, 0)

    greedy_decider = GreedyDecision()
    action = greedy_decider.decide(None, ["前进", "后退", "左转", "右转"], evaluation_func)
    print(f"贪心选择的动作: {action}")

    # Q学习决策示例
    print("\n=== Q学习决策示例 ===")
    q_learner = QLearningDecision()
    
    # 模拟一些学习
    for _ in range(100):
        state = random.randint(1, 10)
        action = q_learner.decide(state, ["前进", "后退"])
        next_state = state + 1 if action == "前进" else state - 1
        reward = 1 if next_state > state else -1
        q_learner.learn(state, action, reward, next_state, ["前进", "后退"])

    # 测试决策
    action = q_learner.decide(5, ["前进", "后退"])
    print(f"Q学习选择的动作: {action}")
    print(f"Q表: {q_learner.q_table}")


if __name__ == "__main__":
    example_usage()
