from mcp import MasterControlProgram

def main():
    """
    主函数，提供命令行交互界面
    """
    print("=====================================")
    print("        多 Agent 协作系统")
    print("=====================================")
    print("功能：")
    print("1. 多 Agent 协同工作")
    print("2. 任务分配与调度")
    print("3. 信息共享与通信")
    print("4. 冲突解决机制")
    print("=====================================")
    print("已注册的 Agent：")
    print("- WeatherAgent：天气查询")
    print("- FileAgent：文件操作")
    print("- MathAgent：数学计算")
    print("=====================================")
    print("输入 'exit' 退出程序")
    print("输入 'agents' 查看已注册的 Agent")
    print("输入 'history' 查看历史任务")
    print("输入 'clear' 清空历史任务")
    print("=====================================")
    
    # 创建 MCP 实例
    mcp = MasterControlProgram()
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n请输入您的任务: ")
            
            # 检查是否退出
            if user_input.lower() == "exit":
                print("感谢使用多 Agent 协作系统，再见！")
                break
            
            # 检查是否查看 Agent 信息
            elif user_input.lower() == "agents":
                agents_info = mcp.get_agents_info()
                print("\n已注册的 Agent：")
                for agent_type, info in agents_info.items():
                    print(f"- {info['name']}：{info['description']}")
                continue
            
            # 检查是否查看历史任务
            elif user_input.lower() == "history":
                history = mcp.get_history()
                print("\n历史任务：")
                if not history:
                    print("暂无历史任务")
                else:
                    for i, item in enumerate(history, 1):
                        print(f"{i}. 任务: {item['task']}")
                        print(f"   结果: {item['result']}")
                continue
            
            # 检查是否清空历史任务
            elif user_input.lower() == "clear":
                mcp.clear_history()
                print("历史任务已清空")
                continue
            
            # 执行任务
            result = mcp.submit_task(user_input)
            
            # 显示结果
            print("\n=====================================")
            print("执行结果:")
            print(result)
            print("=====================================")
            
        except KeyboardInterrupt:
            print("\n程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")
            continue

if __name__ == "__main__":
    main()
