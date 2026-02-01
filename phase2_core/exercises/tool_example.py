#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工具使用示例
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phase2_core.mcp.tool_interface import get_tool_registry
from phase2_core.mcp.tools import initialize_tools


def test_file_reader():
    """
    测试文件读取工具
    """
    print("=== 测试文件读取工具 ===")
    
    # 初始化工具
    initialize_tools()
    
    # 获取工具注册表
    registry = get_tool_registry()
    
    try:
        # 获取文件读取工具
        file_reader = registry.get_tool("file_reader")
        
        # 创建测试文件
        test_file_path = "test_read_file.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试文件，用于测试文件读取工具。\n")
            f.write("第二行内容。\n")
            f.write("第三行内容。")
        
        # 执行文件读取
        result = file_reader.execute(file_path=test_file_path)
        
        print(f"工具执行结果: {result}")
        
        if result["success"]:
            print(f"文件内容: {result['result']['content']}")
            print("测试成功!")
        else:
            print("测试失败!")
        
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_file_writer():
    """
    测试文件写入工具
    """
    print("\n=== 测试文件写入工具 ===")
    
    # 获取工具注册表
    registry = get_tool_registry()
    
    try:
        # 获取文件写入工具
        file_writer = registry.get_tool("file_writer")
        
        # 测试文件路径
        test_file_path = "test_write_file.txt"
        
        # 执行文件写入
        test_content = "这是通过文件写入工具写入的内容。\n第二行内容。"
        result = file_writer.execute(
            file_path=test_file_path,
            content=test_content,
            overwrite=False
        )
        
        print(f"工具执行结果: {result}")
        
        if result["success"]:
            # 验证文件内容
            with open(test_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"文件内容: {content}")
            print("测试成功!")
        else:
            print("测试失败!")
        
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_file_appender():
    """
    测试文件追加工具
    """
    print("\n=== 测试文件追加工具 ===")
    
    # 获取工具注册表
    registry = get_tool_registry()
    
    try:
        # 获取文件追加工具
        file_appender = registry.get_tool("file_appender")
        
        # 测试文件路径
        test_file_path = "test_append_file.txt"
        
        # 先创建文件
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("初始内容。\n")
        
        # 执行文件追加
        append_content = "追加的内容。\n第二行追加内容。"
        result = file_appender.execute(
            file_path=test_file_path,
            content=append_content
        )
        
        print(f"工具执行结果: {result}")
        
        if result["success"]:
            # 验证文件内容
            with open(test_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"文件内容: {content}")
            print("测试成功!")
        else:
            print("测试失败!")
        
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_directory_lister():
    """
    测试目录列表工具
    """
    print("\n=== 测试目录列表工具 ===")
    
    # 获取工具注册表
    registry = get_tool_registry()
    
    try:
        # 获取目录列表工具
        directory_lister = registry.get_tool("directory_lister")
        
        # 执行目录列表
        result = directory_lister.execute(
            directory_path=".",
            show_hidden=False
        )
        
        print(f"工具执行结果: {result}")
        
        if result["success"]:
            items = result["result"]["items"]
            print(f"目录中的项目数: {len(items)}")
            print("前5个项目:")
            for item in items[:5]:
                item_type = "目录" if item["is_directory"] else "文件"
                print(f"- {item['name']} ({item_type}, {item['size']} bytes)")
            print("测试成功!")
        else:
            print("测试失败!")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_command_executor():
    """
    测试命令执行工具
    """
    print("\n=== 测试命令执行工具 ===")
    
    # 获取工具注册表
    registry = get_tool_registry()
    
    try:
        # 获取命令执行工具
        command_executor = registry.get_tool("command_executor")
        
        # 执行命令（根据操作系统选择命令）
        import platform
        if platform.system() == "Windows":
            # Windows命令
            command = "dir /b"
        else:
            # 非Windows命令
            command = "ls -la"
        
        result = command_executor.execute(
            command=command,
            timeout=10
        )
        
        print(f"工具执行结果: {result}")
        
        if result["success"]:
            print(f"命令输出: {result['result']['stdout']}")
            print("测试成功!")
        else:
            print(f"命令执行失败，错误信息: {result['result']['stderr']}")
            print("测试失败!")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")


def main():
    """
    主函数
    """
    print("工具使用示例")
    print("=" * 50)
    
    # 运行测试
    test_file_reader()
    test_file_writer()
    test_file_appender()
    test_directory_lister()
    test_command_executor()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")


if __name__ == "__main__":
    main()
