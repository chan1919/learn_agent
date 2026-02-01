"""
强化学习Agent实现
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple


class RLAgent:
    """
    强化学习Agent
    基于Q-learning算法实现
    """
    
    def __init__(self, state_space_size: int, action_space_size: int, learning_rate: float = 0.1, discount_factor: float = 0.9, exploration_rate: float = 1.0, exploration_decay: float = 0.995):
        """
        初始化强化学习Agent
        
        Args:
            state_space_size: 状态空间大小
            action_space_size: 动作空间大小
            learning_rate: 学习率
            discount_factor: 折扣因子
            exploration_rate: 探索率
            exploration_decay: 探索率衰减因子
        """
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        
        # 初始化Q表
        self.q_table = np.zeros((state_space_size, action_space_size))
        
        # 存储历史轨迹
        self.trajectory = []
    
    def choose_action(self, state: int) -> int:
        """
        根据当前状态选择动作
        
        Args:
            state: 当前状态
            
        Returns:
            选择的动作
        """
        # epsilon-greedy策略
        if np.random.uniform(0, 1) < self.exploration_rate:
            # 探索：随机选择动作
            return np.random.randint(0, self.action_space_size)
        else:
            # 利用：选择Q值最大的动作
            return np.argmax(self.q_table[state, :])
    
    def learn(self, state: int, action: int, reward: float, next_state: int, done: bool):
        """
        从经验中学习
        
        Args:
            state: 当前状态
            action: 选择的动作
            reward: 获得的奖励
            next_state: 下一个状态
            done: 是否结束
        """
        # 存储经验到轨迹
        self.trajectory.append((state, action, reward, next_state, done))
        
        # Q-learning更新规则
        best_next_action = np.argmax(self.q_table[next_state, :])
        td_target = reward + self.discount_factor * self.q_table[next_state, best_next_action] * (1 - done)
        td_error = td_target - self.q_table[state, action]
        
        # 更新Q表
        self.q_table[state, action] += self.learning_rate * td_error
        
        # 衰减探索率
        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(0.01, self.exploration_rate)  # 确保探索率不低于0.01
    
    def get_q_table(self) -> np.ndarray:
        """
        获取Q表
        
        Returns:
            Q表
        """
        return self.q_table
    
    def reset_exploration_rate(self):
        """
        重置探索率
        """
        self.exploration_rate = 1.0
    
    def clear_trajectory(self):
        """
        清空轨迹
        """
        self.trajectory = []


class DeepRLAgent:
    """
    深度强化学习Agent
    基于DQN算法实现（简化版）
    """
    
    def __init__(self, state_space_size: int, action_space_size: int, learning_rate: float = 0.001, discount_factor: float = 0.9, exploration_rate: float = 1.0, exploration_decay: float = 0.995):
        """
        初始化深度强化学习Agent
        
        Args:
            state_space_size: 状态空间大小
            action_space_size: 动作空间大小
            learning_rate: 学习率
            discount_factor: 折扣因子
            exploration_rate: 探索率
            exploration_decay: 探索率衰减因子
        """
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        
        # 这里应该初始化神经网络，现在使用简单的线性模型模拟
        self.weights = np.random.randn(state_space_size, action_space_size) * 0.01
        self.biases = np.zeros(action_space_size)
        
        # 经验回放缓冲区
        self.replay_buffer = []
        self.buffer_size = 1000
    
    def choose_action(self, state: np.ndarray) -> int:
        """
        根据当前状态选择动作
        
        Args:
            state: 当前状态（向量）
            
        Returns:
            选择的动作
        """
        # epsilon-greedy策略
        if np.random.uniform(0, 1) < self.exploration_rate:
            # 探索：随机选择动作
            return np.random.randint(0, self.action_space_size)
        else:
            # 利用：选择Q值最大的动作
            q_values = self._predict(state)
            return np.argmax(q_values)
    
    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        """
        从经验中学习
        
        Args:
            state: 当前状态
            action: 选择的动作
            reward: 获得的奖励
            next_state: 下一个状态
            done: 是否结束
        """
        # 存储经验到回放缓冲区
        self.replay_buffer.append((state, action, reward, next_state, done))
        
        # 限制缓冲区大小
        if len(self.replay_buffer) > self.buffer_size:
            self.replay_buffer.pop(0)
        
        # 从缓冲区中采样批次进行学习
        batch_size = min(32, len(self.replay_buffer))
        batch = np.random.choice(len(self.replay_buffer), batch_size, replace=False)
        
        for i in batch:
            s, a, r, ns, d = self.replay_buffer[i]
            
            # 计算目标Q值
            if d:
                target = r
            else:
                next_q = np.max(self._predict(ns))
                target = r + self.discount_factor * next_q
            
            # 计算当前Q值
            current_q = self._predict(s)[a]
            
            # 简单的梯度下降更新（实际应用中应该使用更复杂的优化器）
            error = target - current_q
            self.weights[:, a] += self.learning_rate * error * s
            self.biases[a] += self.learning_rate * error
        
        # 衰减探索率
        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(0.01, self.exploration_rate)
    
    def _predict(self, state: np.ndarray) -> np.ndarray:
        """
        预测Q值
        
        Args:
            state: 状态
            
        Returns:
            Q值
        """
        # 简单的线性模型，实际应用中应该使用深度神经网络
        return np.dot(state, self.weights) + self.biases
    
    def reset_exploration_rate(self):
        """
        重置探索率
        """
        self.exploration_rate = 1.0
