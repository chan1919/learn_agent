"""
自动化工作流应用场景
"""

import time
from typing import Dict, List, Optional, Any, Callable


class WorkflowNode:
    """
    工作流节点
    """
    
    def __init__(self, name: str, task: Callable):
        """
        初始化工作流节点
        
        Args:
            name: 节点名称
            task: 节点任务函数
        """
        self.name = name
        self.task = task
        self.next_nodes = []  # 后续节点
        self.condition = None  # 条件函数
    
    def add_next(self, next_node, condition: Optional[Callable] = None):
        """
        添加后续节点
        
        Args:
            next_node: 后续节点
            condition: 条件函数，用于判断是否执行该后续节点
        """
        self.next_nodes.append((next_node, condition))
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行节点任务
        
        Args:
            context: 上下文信息
            
        Returns:
            更新后的上下文
        """
        print(f"执行节点: {self.name}")
        
        try:
            # 执行任务
            result = self.task(context)
            
            # 更新上下文
            context[f"{self.name}_result"] = result
            context[f"{self.name}_status"] = "completed"
            context[f"{self.name}_timestamp"] = time.time()
            
            print(f"节点 {self.name} 执行成功，结果: {result}")
            
        except Exception as e:
            # 执行失败
            context[f"{self.name}_status"] = "failed"
            context[f"{self.name}_error"] = str(e)
            context[f"{self.name}_timestamp"] = time.time()
            
            print(f"节点 {self.name} 执行失败，错误: {str(e)}")
        
        return context


class AutomatedWorkflow:
    """
    自动化工作流系统
    """
    
    def __init__(self, name: str):
        """
        初始化自动化工作流
        
        Args:
            name: 工作流名称
        """
        self.name = name
        self.start_node = None  # 起始节点
        self.nodes = {}  # 所有节点
        self.execution_history = []  # 执行历史
    
    def add_node(self, node: WorkflowNode):
        """
        添加节点到工作流
        
        Args:
            node: 工作流节点
        """
        self.nodes[node.name] = node
    
    def set_start_node(self, node_name: str):
        """
        设置起始节点
        
        Args:
            node_name: 节点名称
        """
        if node_name in self.nodes:
            self.start_node = self.nodes[node_name]
            print(f"已设置起始节点: {node_name}")
        else:
            print(f"节点 {node_name} 不存在")
    
    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            initial_context: 初始上下文
            
        Returns:
            最终的上下文
        """
        if not self.start_node:
            print("未设置起始节点")
            return {}
        
        # 初始化上下文
        context = initial_context or {}
        context["workflow_name"] = self.name
        context["start_time"] = time.time()
        
        # 执行工作流
        final_context = self._execute_node(self.start_node, context)
        
        # 更新执行历史
        final_context["end_time"] = time.time()
        final_context["execution_time"] = final_context["end_time"] - final_context["start_time"]
        self.execution_history.append(final_context)
        
        print(f"工作流 {self.name} 执行完成，耗时: {final_context['execution_time']:.2f}秒")
        
        return final_context
    
    def _execute_node(self, node: WorkflowNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        递归执行节点
        
        Args:
            node: 当前节点
            context: 上下文信息
            
        Returns:
            更新后的上下文
        """
        # 执行当前节点
        context = node.execute(context)
        
        # 执行后续节点
        for next_node, condition in node.next_nodes:
            # 检查条件
            if condition is None or condition(context):
                context = self._execute_node(next_node, context)
        
        return context
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """
        获取执行历史
        
        Returns:
            执行历史列表
        """
        return self.execution_history


# 示例工作流定义
def create_example_workflow():
    """
    创建示例工作流
    
    Returns:
        示例工作流
    """
    workflow = AutomatedWorkflow("示例工作流")
    
    # 创建节点
    def task1(context):
        """任务1: 数据收集"""
        return "收集到的数据"
    
    def task2(context):
        """任务2: 数据处理"""
        return "处理后的数据"
    
    def task3(context):
        """任务3: 数据存储"""
        return "数据已存储"
    
    def task4(context):
        """任务4: 错误处理"""
        return "错误已处理"
    
    # 条件函数
    def success_condition(context):
        """成功条件"""
        return context.get("task2_status") == "completed"
    
    def failure_condition(context):
        """失败条件"""
        return context.get("task2_status") == "failed"
    
    # 创建节点
    node1 = WorkflowNode("task1", task1)
    node2 = WorkflowNode("task2", task2)
    node3 = WorkflowNode("task3", task3)
    node4 = WorkflowNode("task4", task4)
    
    # 添加节点到工作流
    workflow.add_node(node1)
    workflow.add_node(node2)
    workflow.add_node(node3)
    workflow.add_node(node4)
    
    # 设置节点关系
    node1.add_next(node2)
    node2.add_next(node3, success_condition)
    node2.add_next(node4, failure_condition)
    
    # 设置起始节点
    workflow.set_start_node("task1")
    
    return workflow
