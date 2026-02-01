#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP使用示例
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phase2_core.mcp.mcp_core import execute_task, get_available_tools


def test_mcp_basic_task():
    """
    测试MCP执行基本任务
    """
    print("=== 测试MCP执行基本任务 ===")
    
    try:
        # 执行一个简单的任务
        task = "请解释什么是人工智能Agent"
        result = execute_task(task)
        
        print(f"任务: {task}")
        print(f"执行结果: {result}")
        
        if result["success"]:
            print(f"摘要: {result['result']['summary']}")
            print("测试成功!")
        else:
            print("测试失败!")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_mcp_file_task():
    """
    测试MCP执行文件操作任务
    """
    print("\n=== 测试MCP执行文件操作任务 ===")
    
    try:
        # 执行文件操作任务
        task = "创建一个名为 'test_mcp_file.txt' 的文件，内容为 '这是通过MCP创建的测试文件'"
        result = execute_task(task)
        
        print(f"任务: {task}")
        print(f"执行结果: {result}")
        
        if result["success"]:
            print(f"摘要: {result['result']['summary']}")
            # 验证文件是否创建
            if os.path.exists("test_mcp_file.txt"):
                with open("test_mcp_file.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                print(f"文件内容: {content}")
                # 清理测试文件
                os.remove("test_mcp_file.txt")
            print("测试成功!")
        else:
            print("测试失败!")
            # 清理测试文件
            if os.path.exists("test_mcp_file.txt"):
                os.remove("test_mcp_file.txt")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        # 清理测试文件
        if os.path.exists("test_mcp_file.txt"):
            os.remove("test_mcp_file.txt")


def test_mcp_command_task():
    """
    测试MCP执行命令执行任务
    """
    print("\n=== 测试MCP执行命令执行任务 ===")
    
    try:
        # 执行命令执行任务
        import platform
        if platform.system() == "Windows":
            # Windows命令
            task = "执行命令 'dir /b' 查看当前目录下的文件"
        else:
            # 非Windows命令
            task = "执行命令 'ls -la' 查看当前目录下的文件"
        
        result = execute_task(task)
        
        print(f"任务: {task}")
        print(f"执行结果: {result}")
        
        if result["success"]:
            print(f"摘要: {result['result']['summary']}")
            print("测试成功!")
        else:
            print("测试失败!")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_mcp_hybrid_task():
    """
    测试MCP执行混合任务
    """
    print("\n=== 测试MCP执行混合任务 ===")
    
    try:
        # 创建一个测试文件
        test_file_path = "test_hybrid_task.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试文件，包含一些文本内容。\n")
            f.write("文件的第二行。\n")
            f.write("文件的第三行。")
        
        # 执行混合任务
        task = f"读取文件 '{test_file_path}' 的内容，然后总结文件内容"
        result = execute_task(task)
        
        print(f"任务: {task}")
        print(f"执行结果: {result}")
        
        if result["success"]:
            print(f"摘要: {result['result']['summary']}")
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


def test_mcp_available_tools():
    """
    测试获取MCP可用的工具
    """
    print("\n=== 测试获取MCP可用的工具 ===")
    
    try:
        # 获取可用的工具
        tools = get_available_tools()
        print(f"可用的工具: {tools}")
        print("测试成功!")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")


def main():
    """
    主函数
    """
    print("MCP使用示例")
    print("=" * 50)
    
    # 运行测试
    test_mcp_basic_task()
    test_mcp_file_task()
    test_mcp_command_task()
    test_mcp_hybrid_task()
    test_mcp_available_tools()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")


if __name__ == "__main__":
    main()
