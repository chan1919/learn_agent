# 第二阶段：核心技术与实现方法

本阶段主要实现了全局LLM模型调用和MCP（Master Control Program）工具调用功能，支持通过统一接口调用不同的LLM模型和执行各种工具操作。

## 目录结构

```
phase2_core/
├── architectures/        # Agent架构实现
│   └── llm_manager.py    # LLM模型管理器
├── algorithms/           # 核心算法实现
│   ├── search_algorithms.py    # 搜索算法
│   ├── planning_algorithms.py  # 规划算法
│   └── decision_algorithms.py  # 决策算法
├── mcp/                  # MCP实现
│   ├── tool_interface.py # 工具接口定义
│   ├── tools.py          # 具体工具实现
│   └── mcp_core.py       # MCP核心实现
├── exercises/            # 练习和示例
│   ├── llm_example.py    # LLM模型调用示例
│   ├── tool_example.py   # 工具使用示例
│   └── mcp_example.py    # MCP使用示例
└── README.md             # 本说明文档
```

## 功能说明

### 1. 全局LLM模型调用

`llm_manager.py` 实现了全局LLM模型调用功能，支持以下特性：

- 支持多种模型提供商：OpenAI、Anthropic、Google Gemini、DeepSeek、本地模型等
- 统一的调用接口：通过 `call_llm` 函数可以调用任何配置的模型
- 自动重试机制：当API调用失败时会自动重试
- 灵活的参数配置：支持设置temperature、max_tokens等参数

#### 使用示例

```python
from phase2_core.architectures.llm_manager import call_llm

# 基本调用
response = call_llm("请解释什么是人工智能Agent")
print(response)

# 带参数调用
response = call_llm(
    "请生成一个关于春天的短诗",
    temperature=0.8,
    max_tokens=200
)
print(response)

# 使用特定提供商
response = call_llm(
    "请解释什么是机器学习",
    provider="deepseek"
)
print(response)
```

### 2. 工具接口和实现

`tool_interface.py` 定义了工具的基本接口，`tools.py` 实现了具体的工具：

- **文件工具**：
  - `file_reader`：读取文件内容
  - `file_writer`：写入文件内容
  - `file_appender`：向文件追加内容
  - `directory_lister`：列出目录内容

- **命令执行工具**：
  - `command_executor`：执行系统命令

#### 使用示例

```python
from phase2_core.mcp.tool_interface import get_tool_registry
from phase2_core.mcp.tools import initialize_tools

# 初始化工具
initialize_tools()

# 获取工具注册表
registry = get_tool_registry()

# 使用文件读取工具
file_reader = registry.get_tool("file_reader")
result = file_reader.execute(file_path="example.txt")
print(result)

# 使用命令执行工具
command_executor = registry.get_tool("command_executor")
result = command_executor.execute(command="dir /b")
print(result)
```

### 3. MCP核心功能

`mcp_core.py` 实现了MCP的核心功能，支持以下特性：

- 任务分析：使用LLM分析任务类型和需求
- 执行计划制定：根据任务分析结果制定执行计划
- 多步骤执行：支持执行包含多个步骤的复杂任务
- 工具调用协调：自动调用所需的工具完成任务
- 结果处理：对执行结果进行总结和处理

#### 使用示例

```python
from phase2_core.mcp.mcp_core import execute_task

# 执行基本任务
result = execute_task("请解释什么是人工智能Agent")
print(result["result"]["summary"])

# 执行文件操作任务
result = execute_task("创建一个名为 'test.txt' 的文件，内容为 '这是测试文件'")
print(result["result"]["summary"])

# 执行命令执行任务
result = execute_task("执行命令 'dir /b' 查看当前目录下的文件")
print(result["result"]["summary"])

# 执行混合任务
result = execute_task("读取文件 'example.txt' 的内容，然后总结文件内容")
print(result["result"]["summary"])
```

### 4. 核心算法

`algorithms/` 目录实现了多种核心算法，支持Agent的决策和规划能力：

#### 4.1 搜索算法

`search_algorithms.py` 实现了以下搜索算法：

- **广度优先搜索**：适合寻找最短路径
- **深度优先搜索**：适合探索所有可能路径
- **A*搜索**：结合启发式信息的高效搜索算法

#### 使用示例

```python
from phase2_core.algorithms.search_algorithms import BreadthFirstSearch, DepthFirstSearch, AStarSearch

# 定义图结构
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

# 启发函数
def heuristic(node, goal):
    return 0  # 简单启发函数

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
```

#### 4.2 规划算法

`planning_algorithms.py` 实现了以下规划算法：

- **简单规划**：基于暴力搜索的简单规划算法
- **目标栈规划**：基于目标分解的规划算法

#### 使用示例

```python
from phase2_core.algorithms.planning_algorithms import SimplePlanning, GoalStackPlanning

# 简单规划示例
def transition_func(state, action):
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
```

#### 4.3 决策算法

`decision_algorithms.py` 实现了以下决策算法：

- **随机决策**：随机选择动作
- **贪心决策**：选择评估值最高的动作
- **极小极大决策**：用于对抗性环境的决策算法
- **Q学习决策**：基于强化学习的决策算法

#### 使用示例

```python
from phase2_core.algorithms.decision_algorithms import RandomDecision, GreedyDecision, QLearningDecision

# 随机决策示例
random_decider = RandomDecision()
action = random_decider.decide(None, ["前进", "后退", "左转", "右转"])
print(f"随机选择的动作: {action}")

# 贪心决策示例
def evaluation_func(state, action):
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
q_learner = QLearningDecision()

# 模拟学习
for _ in range(100):
    state = 5
    action = q_learner.decide(state, ["前进", "后退"])
    next_state = state + 1 if action == "前进" else state - 1
    reward = 1 if next_state > state else -1
    q_learner.learn(state, action, reward, next_state, ["前进", "后退"])

# 测试决策
action = q_learner.decide(5, ["前进", "后退"])
print(f"Q学习选择的动作: {action}")
```

## 运行示例

### 1. 运行LLM模型调用示例

```bash
python phase2_core/exercises/llm_example.py
```

### 2. 运行工具使用示例

```bash
python phase2_core/exercises/tool_example.py
```

### 3. 运行MCP使用示例

```bash
python phase2_core/exercises/mcp_example.py
```

### 4. 运行算法示例

#### 4.1 运行搜索算法示例

```bash
python phase2_core/algorithms/search_algorithms.py
```

#### 4.2 运行规划算法示例

```bash
python phase2_core/algorithms/planning_algorithms.py
```

#### 4.3 运行决策算法示例

```bash
python phase2_core/algorithms/decision_algorithms.py
```

## 配置说明

LLM模型的配置存储在 `config/config.yaml` 文件中，包括：

- 模型提供商的基本URL
- API密钥
- 支持的模型列表
- 超时设置
- 最大重试次数

## 扩展指南

### 添加新的LLM模型提供商

1. 在 `config/config.yaml` 中添加新的模型提供商配置
2. 在 `llm_manager.py` 中添加对应的调用方法
3. 在 `call_methods` 字典中添加新的提供商映射

### 添加新的工具

1. 创建一个新的工具类，继承自 `BaseTool` 或其派生类
2. 实现 `execute` 和 `get_parameters` 方法
3. 在 `initialize_tools` 函数中注册新工具

### 扩展MCP功能

1. 修改 `mcp_core.py` 中的 `analyze_task` 方法，支持新的任务类型
2. 修改 `create_execution_plan` 方法，支持新的执行计划类型
3. 修改 `execute_plan` 方法，支持新的执行步骤类型

### 扩展算法功能

#### 添加新的搜索算法

1. 创建一个新的搜索算法类，继承自 `SearchAlgorithm`
2. 实现 `search` 方法
3. 在需要的地方使用新的搜索算法

#### 添加新的规划算法

1. 创建一个新的规划算法类，继承自 `PlanningAlgorithm`
2. 实现 `plan` 方法
3. 在需要的地方使用新的规划算法

#### 添加新的决策算法

1. 创建一个新的决策算法类，继承自 `DecisionAlgorithm`
2. 实现 `decide` 方法
3. 在需要的地方使用新的决策算法

## 注意事项

1. **API密钥安全**：请确保 `config/config.yaml` 文件中的API密钥不会被提交到版本控制系统
2. **命令执行安全**：`command_executor` 工具可以执行任意系统命令，请谨慎使用
3. **文件操作安全**：文件工具可以读写任意文件，请谨慎使用
4. **超时设置**：对于可能耗时较长的操作，请适当设置超时时间
5. **错误处理**：在使用这些功能时，请确保捕获和处理可能的异常

## 总结

本阶段实现的功能为Agent系统提供了强大的基础能力：

- **全局统一的LLM模型调用接口**：支持多种模型提供商，包括OpenAI、Anthropic、Google Gemini、DeepSeek等
- **丰富的工具集**：支持文件操作（读取、写入、追加、列出目录）和命令执行
- **智能的MCP协调系统**：能够自动分析任务、制定执行计划、协调工具调用和处理结果
- **完整的核心算法实现**：包括搜索算法（广度优先、深度优先、A*）、规划算法（简单规划、目标栈规划）和决策算法（随机决策、贪心决策、极小极大决策、Q学习决策）

这些功能使得Agent系统能够更灵活地处理各种任务，从简单的信息查询到复杂的文件操作、命令执行和决策规划，为构建更智能、更强大的Agent系统奠定了坚实的基础。

通过本阶段的实现，我们建立了一个完整的Agent核心框架，支持：
- 多模型提供商的统一调用
- 丰富的工具集成和使用
- 智能的任务分析和执行
- 强大的算法支持

这为后续的高级功能开发和实际应用场景的实现做好了充分准备。