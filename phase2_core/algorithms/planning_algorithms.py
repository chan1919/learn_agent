#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
规划算法实现
"""

from typing import List, Dict, Any, Optional, Callable, Tuple


class PlanningAlgorithm:
    """
    规划算法基类
    """

    def plan(self, initial_state: Any, goal_state: Any, **kwargs) -> List[Dict[str, Any]]:
        """
        生成从初始状态到目标状态的规划

        参数:
            initial_state: 初始状态
            goal_state: 目标状态
            **kwargs: 额外参数

        返回:
            规划步骤列表，每个步骤包含'action'和'next_state'字段
        """
        raise NotImplementedError


class SimplePlanning(PlanningAlgorithm):
    """
    简单规划算法
    """

    def plan(self, initial_state: Any, goal_state: Any, actions: List[str], transition_func: Callable, **kwargs) -> List[Dict[str, Any]]:
        """
        生成简单规划

        参数:
            initial_state: 初始状态
            goal_state: 目标状态
            actions: 可用动作列表
            transition_func: 状态转移函数，接收当前状态和动作，返回新状态
            **kwargs: 额外参数

        返回:
            规划步骤列表
        """
        plan = []
        current_state = initial_state

        # 简单的暴力搜索规划
        max_steps = kwargs.get('max_steps', 10)
        step_count = 0

        while current_state != goal_state and step_count < max_steps:
            # 尝试每个动作
            for action in actions:
                next_state = transition_func(current_state, action)
                if next_state == goal_state:
                    # 找到目标，添加最后一步
                    plan.append({
                        'action': action,
                        'next_state': next_state
                    })
                    return plan
                elif next_state != current_state:  # 避免循环
                    # 添加这一步并继续搜索
                    plan.append({
                        'action': action,
                        'next_state': next_state
                    })
                    current_state = next_state
                    step_count += 1
                    break
            else:
                # 所有动作都尝试过了，无法到达目标
                break

        return plan


class GoalStackPlanning(PlanningAlgorithm):
    """
    目标栈规划算法
    """

    def __init__(self):
        """
        初始化目标栈规划算法
        """
        self.stack = []
        self.current_state = None
        self.actions = []
        self.operators = {}

    def plan(self, initial_state: Any, goal_state: Any, operators: Dict[str, Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        使用目标栈规划算法生成规划

        参数:
            initial_state: 初始状态
            goal_state: 目标状态
            operators: 操作符字典，每个操作符包含'preconditions'和'effects'
            **kwargs: 额外参数

        返回:
            规划步骤列表
        """
        self.current_state = initial_state
        self.operators = operators
        self.stack = [goal_state]
        self.actions = []

        # 执行规划
        while self.stack:
            top = self.stack.pop()
            
            if isinstance(top, str) and top in self.operators:
                # 处理操作符
                operator = top
                if self._satisfies_preconditions(operator):
                    # 应用操作符
                    self._apply_operator(operator)
                    self.actions.append({
                        'action': operator,
                        'next_state': self.current_state.copy()
                    })
                else:
                    # 将操作符放回栈中
                    self.stack.append(operator)
                    # 将前置条件加入栈中
                    preconditions = self.operators[operator]['preconditions']
                    for precondition in reversed(preconditions):
                        self.stack.append(precondition)
            elif isinstance(top, dict):
                # 处理目标状态
                goal = top
                if self._satisfies_goal(goal):
                    # 目标已满足，继续
                    pass
                else:
                    # 目标未满足，找到能满足目标的操作符
                    applicable_operators = self._find_applicable_operators(goal)
                    if applicable_operators:
                        # 选择第一个适用的操作符
                        operator = applicable_operators[0]
                        self.stack.append(operator)
                    else:
                        # 没有适用的操作符
                        break
            elif isinstance(top, tuple):
                # 处理前置条件
                precondition = top
                if self._satisfies_precondition(precondition):
                    # 前置条件已满足，继续
                    pass
                else:
                    # 前置条件未满足，找到能满足前置条件的操作符
                    applicable_operators = self._find_applicable_operators_for_precondition(precondition)
                    if applicable_operators:
                        # 选择第一个适用的操作符
                        operator = applicable_operators[0]
                        self.stack.append(operator)
                    else:
                        # 没有适用的操作符
                        break

        return self.actions

    def _satisfies_goal(self, goal: Dict[str, Any]) -> bool:
        """
        检查当前状态是否满足目标

        参数:
            goal: 目标状态

        返回:
            是否满足目标
        """
        for key, value in goal.items():
            if self.current_state.get(key) != value:
                return False
        return True

    def _satisfies_precondition(self, precondition: Tuple[str, Any]) -> bool:
        """
        检查当前状态是否满足前置条件

        参数:
            precondition: 前置条件，格式为(key, value)

        返回:
            是否满足前置条件
        """
        key, value = precondition
        return self.current_state.get(key) == value

    def _satisfies_preconditions(self, operator: str) -> bool:
        """
        检查当前状态是否满足操作符的所有前置条件

        参数:
            operator: 操作符名称

        返回:
            是否满足所有前置条件
        """
        preconditions = self.operators[operator]['preconditions']
        for precondition in preconditions:
            if not self._satisfies_precondition(precondition):
                return False
        return True

    def _apply_operator(self, operator: str) -> None:
        """
        应用操作符到当前状态

        参数:
            operator: 操作符名称
        """
        effects = self.operators[operator]['effects']
        for key, value in effects.items():
            self.current_state[key] = value

    def _find_applicable_operators(self, goal: Dict[str, Any]) -> List[str]:
        """
        找到能满足目标的操作符

        参数:
            goal: 目标状态

        返回:
            适用的操作符列表
        """
        applicable = []
        for operator_name, operator in self.operators.items():
            effects = operator['effects']
            # 检查操作符的效果是否包含目标的所有内容
            satisfies = True
            for key, value in goal.items():
                if effects.get(key) != value:
                    satisfies = False
                    break
            if satisfies:
                applicable.append(operator_name)
        return applicable

    def _find_applicable_operators_for_precondition(self, precondition: Tuple[str, Any]) -> List[str]:
        """
        找到能满足前置条件的操作符

        参数:
            precondition: 前置条件

        返回:
            适用的操作符列表
        """
        applicable = []
        key, value = precondition
        for operator_name, operator in self.operators.items():
            effects = operator['effects']
            if effects.get(key) == value:
                applicable.append(operator_name)
        return applicable


# 示例使用
def example_usage():
    """
    示例使用
    """
    # 简单规划示例
    print("=== 简单规划示例 ===")
    def transition_func(state, action):
        """
        状态转移函数
        """
        if action == "前进":
            return state + 1
        elif action == "后退":
            return state - 1
        else:
            return state

    simple_planner = SimplePlanning()
    plan = simple_planner.plan(
        initial_state=1,
        goal_state=5,
        actions=["前进", "后退"],
        transition_func=transition_func
    )
    print(f"简单规划结果: {plan}")

    # 目标栈规划示例
    print("\n=== 目标栈规划示例 ===")
    initial_state = {"at": "A"}
    goal_state = {"at": "C"}
    operators = {
        "move_A_to_B": {
            "preconditions": [("at", "A")],
            "effects": {"at": "B"}
        },
        "move_B_to_C": {
            "preconditions": [("at", "B")],
            "effects": {"at": "C"}
        }
    }

    gsp = GoalStackPlanning()
    plan = gsp.plan(
        initial_state=initial_state,
        goal_state=goal_state,
        operators=operators
    )
    print(f"目标栈规划结果: {plan}")


if __name__ == "__main__":
    example_usage()
