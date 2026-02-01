"""
主程序
"""

from agent import LLMAssistant


def main():
    """
    主函数
    """
    # 初始化智能助手
    assistant = LLMAssistant()
    
    print(f"{assistant.name} 已启动，输入 '退出' 结束对话")
    print("=" * 50)
    
    # 主对话循环
    while True:
        # 获取用户输入
        user_input = input("用户: ")
        
        # 检查是否退出
        if user_input.lower() == "退出":
            print(f"{assistant.name}: 再见！")
            break
        
        # 处理用户输入
        response = assistant.chat(user_input)
        
        # 输出助手响应
        print(f"{assistant.name}: {response}")
        print("=" * 50)


if __name__ == "__main__":
    main()
