import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """项目配置类"""
    
    # API 密钥配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YourKey")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YourKey")
    
    # 模型配置
    OPENAI_MODEL = "gpt-4"
    ANTHROPIC_MODEL = "claude-3-opus-20240229"
    
    # MCP 配置
    MCP_MAX_AGENTS = 10
    MCP_MAX_TASKS = 100
    MCP_TIMEOUT = 30.0
    
    # Agent 配置
    AGENT_MAX_RETRIES = 3
    AGENT_TIMEOUT = 10.0
    
    # 工具配置
    TOOLS_ENABLED = True
    MAX_TOOL_CALLS = 10
    
    # 代理配置
    PROXY_ENABLED = False
    PROXY_URL = "http://localhost:7890"
    
    # 日志配置
    LOG_LEVEL = "INFO"

# 创建全局配置实例
config = Config()
