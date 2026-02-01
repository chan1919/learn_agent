#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理器测试文件
"""

from config_manager import get_config_manager


def test_config_manager():
    """
    测试配置管理器功能
    """
    print("=== 配置管理器测试 ===")

    # 获取配置管理器实例
    config_manager = get_config_manager()

    # 1. 测试获取完整配置
    print("\n1. 测试获取完整配置:")
    config = config_manager.get_config()
    print(f"配置版本: {config.get('version')}")
    print(f"模型数量: {len(config.get('models', {}))}")

    # 2. 测试获取所有模型配置
    print("\n2. 测试获取所有模型配置:")
    all_models = config_manager.get_all_models()
    for provider, model_config in all_models.items():
        print(f"- {provider}: {model_config.get('name')} (URL: {model_config.get('base_url')})")

    # 3. 测试获取指定模型配置
    print("\n3. 测试获取指定模型配置:")
    test_providers = ['openai', 'openai_proxy', 'anthropic', 'gemini', 'local_model', 'deepseek']
    for provider in test_providers:
        model_config = config_manager.get_model_config(provider)
        if model_config:
            print(f"{provider}: 成功获取配置")
            print(f"  名称: {model_config.get('name')}")
            print(f"  基础URL: {model_config.get('base_url')}")
            print(f"  支持的模型: {model_config.get('models')}")
            print(f"  超时: {model_config.get('timeout')}秒")
            print(f"  最大重试: {model_config.get('max_retries')}次")
        else:
            print(f"{provider}: 配置不存在")

    # 4. 测试获取默认配置
    print("\n4. 测试获取默认配置:")
    default_config = config_manager.get_default_config()
    print(f"默认模型提供商: {default_config.get('model_provider')}")
    print(f"默认模型: {default_config.get('default_model')}")
    print(f"默认温度: {default_config.get('temperature')}")
    print(f"默认最大token: {default_config.get('max_tokens')}")
    print(f"默认top_p: {default_config.get('top_p')}")

    # 5. 测试获取默认提供商和模型
    print("\n5. 测试获取默认提供商和模型:")
    default_provider = config_manager.get_default_provider()
    default_model = config_manager.get_default_model()
    print(f"默认提供商: {default_provider}")
    print(f"默认模型: {default_model}")

    # 6. 测试验证配置
    print("\n6. 测试验证配置:")
    is_valid = config_manager.validate_config()
    print(f"配置是否有效: {is_valid}")

    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_config_manager()