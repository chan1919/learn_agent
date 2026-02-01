# 多 Agent 协作系统项目

## 项目简介

这是一个多 Agent 协作系统项目，基于 MCP (Master Control Program) 架构，多个 Agent 可以协同工作完成复杂任务。

## 功能特性

- 多 Agent 协同工作
- 任务分配与调度
- 信息共享与通信
- 冲突解决机制
- 性能监控与优化

## 目录结构

```
project2/
├── README.md            # 项目说明
├── requirements.txt     # 依赖项
├── main.py              # 主入口
├── mcp.py               # 主控程序
├── agents/              # Agent 目录
│   ├── base_agent.py    # 基础 Agent 类
│   ├── weather_agent.py # 天气查询 Agent
│   ├── file_agent.py    # 文件操作 Agent
│   └── math_agent.py    # 数学计算 Agent
├── tools.py             # 工具函数
├── config.py            # 配置文件
└── test_mcp.py          # 测试文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

在 `config.py` 文件中配置你的 API 密钥。

### 3. 运行项目

```bash
python main.py
```

### 4. 测试项目

```bash
python test_mcp.py
```

## 使用示例

```python
from mcp import MasterControlProgram

# 创建 MCP 实例
mcp = MasterControlProgram()

# 提交任务
result = mcp.submit_task("查询北京的天气并计算 1+2*3")
print(result)
```

## 项目架构

- **MCP**：主控程序，负责任务分配、Agent 管理和协作协调
- **基础 Agent**：所有 Agent 的基类，提供通用功能
- **专业 Agent**：负责特定领域的任务，如天气查询、文件操作等
- **工具系统**：提供各种功能模块，供 Agent 使用
- **配置管理**：处理 API 密钥和其他配置信息

## 扩展指南

### 添加新 Agent

1. 在 `agents/` 目录中创建新的 Agent 类
2. 继承 `BaseAgent` 类并实现必要的方法
3. 在 MCP 中注册新 Agent

### 调整任务分配策略

修改 `mcp.py` 中的任务分配逻辑，根据实际需求调整策略。

### 添加新工具

在 `tools.py` 中创建新的工具函数，并在需要的 Agent 中使用。

## 技术栈

- Python 3.8+
- 大语言模型 API（如 OpenAI、Anthropic 等）
- 各种工具库

## 注意事项

- 确保 API 密钥的安全性
- 合理使用 API 调用，避免过度请求
- 定期更新依赖项以获取最新功能和安全修复
