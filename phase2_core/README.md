# 第二阶段：核心技术与实现方法

本阶段主要实现了全局LLM模型调用和MCP（Master Control Program）工具调用功能，支持通过统一接口调用不同的LLM模型和执行各种工具操作。

## 目录结构

```
phase2_core/
├── architectures/        # Agent架构实现
│   └── llm_manager.py    # LLM模型管理器
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

## 注意事项

1. **API密钥安全**：请确保 `config/config.yaml` 文件中的API密钥不会被提交到版本控制系统
2. **命令执行安全**：`command_executor` 工具可以执行任意系统命令，请谨慎使用
3. **文件操作安全**：文件工具可以读写任意文件，请谨慎使用
4. **超时设置**：对于可能耗时较长的操作，请适当设置超时时间
5. **错误处理**：在使用这些功能时，请确保捕获和处理可能的异常

## 总结

本阶段实现的功能为Agent系统提供了强大的基础能力：

- 全局统一的LLM模型调用接口，支持多种模型提供商
- 丰富的工具集，支持文件操作和命令执行
- 智能的MCP协调系统，能够自动分析任务并执行相应的操作

这些功能使得Agent系统能够更灵活地处理各种任务，从简单的信息查询到复杂的文件操作和命令执行，为构建更智能、更强大的Agent系统奠定了基础。