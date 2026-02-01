from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class ToolError(Exception):
    """
    工具执行异常
    """
    pass


class BaseTool(ABC):
    """
    工具基类，所有工具都需要继承此类
    """

    def __init__(self, name: str, description: str):
        """
        初始化工具

        参数:
            name: 工具名称
            description: 工具描述
        """
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行工具

        参数:
            **kwargs: 工具执行参数

        返回:
            执行结果字典，包含'success'和'result'字段

        异常:
            ToolError: 如果执行失败
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        获取工具信息

        返回:
            工具信息字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_parameters()
        }

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """
        获取工具参数信息

        返回:
            参数信息字典
        """
        pass


class FileTool(BaseTool):
    """
    文件操作工具基类
    """

    def __init__(self, name: str, description: str):
        """
        初始化文件工具

        参数:
            name: 工具名称
            description: 工具描述
        """
        super().__init__(name, description)


class ExecTool(BaseTool):
    """
    命令执行工具基类
    """

    def __init__(self, name: str, description: str):
        """
        初始化命令执行工具

        参数:
            name: 工具名称
            description: 工具描述
        """
        super().__init__(name, description)


class APITool(BaseTool):
    """
    API调用工具基类
    """

    def __init__(self, name: str, description: str):
        """
        初始化API调用工具

        参数:
            name: 工具名称
            description: 工具描述
        """
        super().__init__(name, description)


class ToolRegistry:
    """
    工具注册表，用于管理所有可用的工具
    """

    def __init__(self):
        """
        初始化工具注册表
        """
        self.tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        """
        注册工具

        参数:
            tool: 工具实例

        异常:
            ToolError: 如果工具名称已存在
        """
        if tool.name in self.tools:
            raise ToolError(f"工具名称 '{tool.name}' 已存在")
        self.tools[tool.name] = tool

    def unregister_tool(self, tool_name: str):
        """
        注销工具

        参数:
            tool_name: 工具名称

        异常:
            ToolError: 如果工具不存在
        """
        if tool_name not in self.tools:
            raise ToolError(f"工具 '{tool_name}' 不存在")
        del self.tools[tool_name]

    def get_tool(self, tool_name: str) -> BaseTool:
        """
        获取工具

        参数:
            tool_name: 工具名称

        返回:
            工具实例

        异常:
            ToolError: 如果工具不存在
        """
        tool = self.tools.get(tool_name)
        if not tool:
            raise ToolError(f"工具 '{tool_name}' 不存在")
        return tool

    def get_all_tools(self) -> Dict[str, BaseTool]:
        """
        获取所有工具

        返回:
            工具字典，键为工具名称，值为工具实例
        """
        return self.tools

    def get_tool_info_list(self) -> List[Dict[str, Any]]:
        """
        获取所有工具信息列表

        返回:
            工具信息列表
        """
        return [tool.get_info() for tool in self.tools.values()]


# 全局工具注册表实例
_tool_registry = None


def get_tool_registry() -> ToolRegistry:
    """
    获取全局工具注册表实例

    返回:
        工具注册表实例
    """
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry
