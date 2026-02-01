from agent import SmartAssistantAgent

def main():
    """
    主函数，提供命令行交互界面
    """
    print("=====================================")
    print("        智能助手 Agent")
    print("=====================================")
    print("功能：")
    print("1. 查询天气")
    print("2. 读取文件")
    print("3. 写入文件")
    print("4. 获取当前时间")
    print("5. 数学计算")
    print("6. 其他通用任务")
    print("=====================================")
    print("输入 'exit' 退出程序")
    print("=====================================")
    
    # 创建 Agent 实例
    agent = SmartAssistantAgent()
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n请输入您的任务: ")
            
            # 检查是否退出
            if user_input.lower() == "exit":
                print("感谢使用智能助手，再见！")
                break
            
            # 执行任务
            result = agent.execute_task(user_input)
            
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
