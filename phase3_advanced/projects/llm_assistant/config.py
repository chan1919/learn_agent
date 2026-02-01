"""
配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_api_key")
MODEL_NAME = "gpt-4"

# Agent配置
AGENT_NAME = "智能助手"
MAX_MEMORY_SIZE = 100  # 最大记忆大小

# 工具配置
TOOL_TIMEOUT = 30  # 工具执行超时时间（秒）

# 对话配置
TEMPERATURE = 0.7  # 生成温度
MAX_TOKENS = 1000  # 最大生成 tokens
