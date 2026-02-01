import os
import subprocess
from typing import Dict, Any, Optional

from .tool_interface import FileTool, ExecTool, ToolError


class FileReaderTool(FileTool):
    """
    文件读取工具
    """

    def __init__(self):
        """
        初始化文件读取工具
        """
        super().__init__(
            name="file_reader",
            description="读取文件内容"
        )

    def execute(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        执行文件读取

        参数:
            file_path: 文件路径
            **kwargs: 额外参数

        返回:
            执行结果字典

        异常:
            ToolError: 如果读取失败
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise ToolError(f"文件 '{file_path}' 不存在")

            # 检查是否是文件
            if not os.path.isfile(file_path):
                raise ToolError(f"路径 '{file_path}' 不是文件")

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "success": True,
                "result": {
                    "file_path": file_path,
                    "content": content,
                    "size": len(content)
                }
            }
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"读取文件失败: {str(e)}")

    def get_parameters(self) -> Dict[str, Any]:
        """
        获取工具参数信息

        返回:
            参数信息字典
        """
        return {
            "file_path": {
                "type": "string",
                "description": "要读取的文件路径",
                "required": True
            }
        }


class FileWriterTool(FileTool):
    """
    文件写入工具
    """

    def __init__(self):
        """
        初始化文件写入工具
        """
        super().__init__(
            name="file_writer",
            description="写入文件内容"
        )

    def execute(self, file_path: str, content: str, overwrite: bool = False, **kwargs) -> Dict[str, Any]:
        """
        执行文件写入

        参数:
            file_path: 文件路径
            content: 要写入的内容
            overwrite: 是否覆盖已存在的文件
            **kwargs: 额外参数

        返回:
            执行结果字典

        异常:
            ToolError: 如果写入失败
        """
        try:
            # 检查文件是否已存在
            if os.path.exists(file_path) and not overwrite:
                raise ToolError(f"文件 '{file_path}' 已存在，请设置 overwrite=True 以覆盖")

            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "success": True,
                "result": {
                    "file_path": file_path,
                    "size": len(content),
                    "overwrite": overwrite
                }
            }
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"写入文件失败: {str(e)}")

    def get_parameters(self) -> Dict[str, Any]:
        """
        获取工具参数信息

        返回:
            参数信息字典
        """
        return {
            "file_path": {
                "type": "string",
                "description": "要写入的文件路径",
                "required": True
            },
            "content": {
                "type": "string",
                "description": "要写入的内容",
                "required": True
            },
            "overwrite": {
                "type": "boolean",
                "description": "是否覆盖已存在的文件",
                "required": False,
                "default": False
            }
        }


class FileAppenderTool(FileTool):
    """
    文件追加工具
    """

    def __init__(self):
        """
        初始化文件追加工具
        """
        super().__init__(
            name="file_appender",
            description="向文件追加内容"
        )

    def execute(self, file_path: str, content: str, **kwargs) -> Dict[str, Any]:
        """
        执行文件追加

        参数:
            file_path: 文件路径
            content: 要追加的内容
            **kwargs: 额外参数

        返回:
            执行结果字典

        异常:
            ToolError: 如果追加失败
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            # 追加文件
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)

            return {
                "success": True,
                "result": {
                    "file_path": file_path,
                    "added_size": len(content)
                }
            }
        except Exception as e:
            raise ToolError(f"追加文件失败: {str(e)}")

    def get_parameters(self) -> Dict[str, Any]:
        """
        获取工具参数信息

        返回:
            参数信息字典
        """
        return {
            "file_path": {
                "type": "string",
                "description": "要追加的文件路径",
                "required": True
            },
            "content": {
                "type": "string",
                "description": "要追加的内容",
                "required": True
            }
        }


class CommandExecutorTool(ExecTool):
    """
    命令执行工具
    """

    def __init__(self):
        """
        初始化命令执行工具
        """
        super().__init__(
            name="command_executor",
            description="执行系统命令"
        )

    def execute(self, command: str, cwd: Optional[str] = None, timeout: int = 30, **kwargs) -> Dict[str, Any]:
        """
        执行命令

        参数:
            command: 要执行的命令
            cwd: 工作目录
            timeout: 超时时间（秒）
            **kwargs: 额外参数

        返回:
            执行结果字典

        异常:
            ToolError: 如果执行失败
        """
        try:
            # 执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout
            )

            # 检查执行结果
            success = result.returncode == 0

            return {
                "success": success,
                "result": {
                    "command": command,
                    "cwd": cwd,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            }
        except subprocess.TimeoutExpired:
            raise ToolError(f"命令执行超时: {timeout}秒")
        except Exception as e:
            raise ToolError(f"执行命令失败: {str(e)}")

    def get_parameters(self) -> Dict[str, Any]:
        """
        获取工具参数信息

        返回:
            参数信息字典
        """
        return {
            "command": {
                "type": "string",
                "description": "要执行的命令",
                "required": True
            },
            "cwd": {
                "type": "string",
                "description": "工作目录",
                "required": False
            },
            "timeout": {
                "type": "integer",
                "description": "超时时间（秒）",
                "required": False,
                "default": 30
            }
        }


class DirectoryListerTool(FileTool):
    """
    目录列表工具
    """

    def __init__(self):
        """
        初始化目录列表工具
        """
        super().__init__(
            name="directory_lister",
            description="列出目录内容"
        )

    def execute(self, directory_path: str, show_hidden: bool = False, **kwargs) -> Dict[str, Any]:
        """
        执行目录列表

        参数:
            directory_path: 目录路径
            show_hidden: 是否显示隐藏文件
            **kwargs: 额外参数

        返回:
            执行结果字典

        异常:
            ToolError: 如果列出失败
        """
        try:
            # 检查目录是否存在
            if not os.path.exists(directory_path):
                raise ToolError(f"目录 '{directory_path}' 不存在")

            # 检查是否是目录
            if not os.path.isdir(directory_path):
                raise ToolError(f"路径 '{directory_path}' 不是目录")

            # 列出目录内容
            items = []
            for item in os.listdir(directory_path):
                # 跳过隐藏文件（如果不显示）
                if not show_hidden and item.startswith('.'):
                    continue

                item_path = os.path.join(directory_path, item)
                items.append({
                    "name": item,
                    "path": item_path,
                    "is_directory": os.path.isdir(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                })

            return {
                "success": True,
                "result": {
                    "directory_path": directory_path,
                    "items": items,
                    "total_items": len(items)
                }
            }
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"列出目录失败: {str(e)}")

    def get_parameters(self) -> Dict[str, Any]:
        """
        获取工具参数信息

        返回:
            参数信息字典
        """
        return {
            "directory_path": {
                "type": "string",
                "description": "要列出的目录路径",
                "required": True
            },
            "show_hidden": {
                "type": "boolean",
                "description": "是否显示隐藏文件",
                "required": False,
                "default": False
            }
        }


# 工具初始化函数
def initialize_tools():
    """
    初始化并注册所有工具
    """
    from .tool_interface import get_tool_registry

    registry = get_tool_registry()

    # 注册文件工具
    registry.register_tool(FileReaderTool())
    registry.register_tool(FileWriterTool())
    registry.register_tool(FileAppenderTool())
    registry.register_tool(DirectoryListerTool())

    # 注册命令执行工具
    registry.register_tool(CommandExecutorTool())
