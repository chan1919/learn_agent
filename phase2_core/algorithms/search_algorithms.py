#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
搜索算法实现
"""

from typing import List, Tuple, Dict, Any, Optional


class SearchAlgorithm:
    """
    搜索算法基类
    """

    def search(self, start_state: Any, goal_state: Any, **kwargs) -> List[Any]:
        """
        搜索从起始状态到目标状态的路径

        参数:
            start_state: 起始状态
            goal_state: 目标状态
            **kwargs: 额外参数

        返回:
            从起始状态到目标状态的路径
        """
        raise NotImplementedError


class BreadthFirstSearch(SearchAlgorithm):
    """
    广度优先搜索算法
    """

    def search(self, start_state: Any, goal_state: Any, get_neighbors: callable, **kwargs) -> List[Any]:
        """
        执行广度优先搜索

        参数:
            start_state: 起始状态
            goal_state: 目标状态
            get_neighbors: 获取邻居状态的函数
            **kwargs: 额外参数

        返回:
            从起始状态到目标状态的路径
        """
        from collections import deque

        # 检查起始状态是否为目标状态
        if start_state == goal_state:
            return [start_state]

        # 初始化队列和访问集合
        queue = deque([(start_state, [start_state])])
        visited = set([start_state])

        while queue:
            current_state, path = queue.popleft()

            # 获取邻居状态
            neighbors = get_neighbors(current_state)

            for neighbor in neighbors:
                if neighbor == goal_state:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        # 未找到路径
        return []


class DepthFirstSearch(SearchAlgorithm):
    """
    深度优先搜索算法
    """

    def search(self, start_state: Any, goal_state: Any, get_neighbors: callable, **kwargs) -> List[Any]:
        """
        执行深度优先搜索

        参数:
            start_state: 起始状态
            goal_state: 目标状态
            get_neighbors: 获取邻居状态的函数
            **kwargs: 额外参数

        返回:
            从起始状态到目标状态的路径
        """

        # 检查起始状态是否为目标状态
        if start_state == goal_state:
            return [start_state]

        # 初始化栈和访问集合
        stack = [(start_state, [start_state])]
        visited = set([start_state])

        while stack:
            current_state, path = stack.pop()

            # 获取邻居状态
            neighbors = get_neighbors(current_state)

            for neighbor in neighbors:
                if neighbor == goal_state:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        # 未找到路径
        return []


class AStarSearch(SearchAlgorithm):
    """
    A*搜索算法
    """

    def search(self, start_state: Any, goal_state: Any, get_neighbors: callable, heuristic: callable, **kwargs) -> List[Any]:
        """
        执行A*搜索

        参数:
            start_state: 起始状态
            goal_state: 目标状态
            get_neighbors: 获取邻居状态的函数
            heuristic: 启发函数，估计从当前状态到目标状态的代价
            **kwargs: 额外参数

        返回:
            从起始状态到目标状态的路径
        """
        import heapq

        # 检查起始状态是否为目标状态
        if start_state == goal_state:
            return [start_state]

        # 初始化优先队列和访问集合
        # 队列元素: (总代价, 当前代价, 当前状态, 路径)
        priority_queue = []
        heapq.heappush(priority_queue, (heuristic(start_state, goal_state), 0, start_state, [start_state]))
        visited = {start_state: 0}

        while priority_queue:
            _, current_cost, current_state, path = heapq.heappop(priority_queue)

            # 获取邻居状态
            neighbors = get_neighbors(current_state)

            for neighbor in neighbors:
                if neighbor == goal_state:
                    return path + [neighbor]

                # 计算新的代价
                new_cost = current_cost + 1  # 假设每步代价为1
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    total_cost = new_cost + heuristic(neighbor, goal_state)
                    heapq.heappush(priority_queue, (total_cost, new_cost, neighbor, path + [neighbor]))

        # 未找到路径
        return []


# 示例使用
def example_usage():
    """
    示例使用
    """
    # 定义一个简单的图
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # 获取邻居的函数
    def get_neighbors(node):
        return graph.get(node, [])

    # 启发函数（曼哈顿距离的简化版）
    def heuristic(node, goal):
        # 这里使用简单的启发函数，实际应用中应该使用更合适的启发函数
        return 0

    # 测试广度优先搜索
    bfs = BreadthFirstSearch()
    bfs_path = bfs.search('A', 'F', get_neighbors)
    print(f"广度优先搜索路径: {bfs_path}")

    # 测试深度优先搜索
    dfs = DepthFirstSearch()
    dfs_path = dfs.search('A', 'F', get_neighbors)
    print(f"深度优先搜索路径: {dfs_path}")

    # 测试A*搜索
    astar = AStarSearch()
    astar_path = astar.search('A', 'F', get_neighbors, heuristic)
    print(f"A*搜索路径: {astar_path}")


if __name__ == "__main__":
    example_usage()
