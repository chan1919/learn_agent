#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM模型调用示例
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phase2_core.architectures.llm_manager import call_llm, get_available_llm_providers, get_available_llm_models


def test_basic_llm_call():
    """
    测试基本的LLM模型调用
    """
    print("=== 测试基本的LLM模型调用 ===")
    
    # 简单的提示词
    prompt = "请解释什么是人工智能Agent"
    
    try:
        # 调用LLM
        response = call_llm(prompt)
        print(f"提示词: {prompt}")
        print(f"响应: {response}")
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_llm_with_parameters():
    """
    测试带参数的LLM模型调用
    """
    print("\n=== 测试带参数的LLM模型调用 ===")
    
    # 带参数的提示词
    prompt = "请生成一个50字以内的关于春天的短诗"
    
    try:
        # 调用LLM，设置参数
        response = call_llm(
            prompt,
            temperature=0.8,  # 增加随机性
            max_tokens=200     # 限制最大 tokens
        )
        print(f"提示词: {prompt}")
        print(f"响应: {response}")
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_llm_providers():
    """
    测试获取可用的LLM提供商
    """
    print("\n=== 测试获取可用的LLM提供商 ===")
    
    try:
        # 获取可用的提供商
        providers = get_available_llm_providers()
        print(f"可用的LLM提供商: {providers}")
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_llm_models():
    """
    测试获取可用的LLM模型
    """
    print("\n=== 测试获取可用的LLM模型 ===")
    
    try:
        # 获取默认提供商的可用模型
        models = get_available_llm_models()
        print(f"默认提供商的可用模型: {models}")
        
        # 获取特定提供商的可用模型
        if 'deepseek' in get_available_llm_providers():
            deepseek_models = get_available_llm_models('deepseek')
            print(f"DeepSeek的可用模型: {deepseek_models}")
        
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {str(e)}")


def test_specific_provider():
    """
    测试使用特定的LLM提供商
    """
    print("\n=== 测试使用特定的LLM提供商 ===")
    
    # 检查是否有DeepSeek提供商
    if 'deepseek' in get_available_llm_providers():
        prompt = "请解释什么是机器学习"
        
        try:
            # 使用DeepSeek提供商
            response = call_llm(prompt, provider='deepseek')
            print(f"提示词: {prompt}")
            print(f"使用DeepSeek的响应: {response}")
            print("测试成功!")
        except Exception as e:
            print(f"测试失败: {str(e)}")
    else:
        print("DeepSeek提供商不可用，跳过测试")


def main():
    """
    主函数
    """
    print("LLM模型调用示例")
    print("=" * 50)
    
    # 运行测试
    test_basic_llm_call()
    test_llm_with_parameters()
    test_llm_providers()
    test_llm_models()
    test_specific_provider()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")


if __name__ == "__main__":
    main()
