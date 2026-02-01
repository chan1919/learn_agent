import os
import sys
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.config_manager import get_config_manager


class LLMError(Exception):
    """
    LLM调用异常
    """
    pass


class LLMManager:
    """
    LLM模型管理器，负责管理和调用不同的LLM模型
    """

    def __init__(self):
        """
        初始化LLM管理器
        """
        self.config_manager = get_config_manager()
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        创建带有重试机制的requests会话

        返回:
            配置好的requests会话
        """
        session = requests.Session()
        retry = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_model_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        获取模型配置

        参数:
            provider: 模型提供商名称，如果为None则使用默认提供商

        返回:
            模型配置字典

        异常:
            LLMError: 如果无法获取模型配置
        """
        if provider is None:
            provider = self.config_manager.get_default_provider()

        model_config = self.config_manager.get_model_config(provider)
        if not model_config:
            raise LLMError(f"无法获取模型提供商 '{provider}' 的配置")

        return model_config

    def call_openai(self, config: Dict[str, Any], prompt: str, model: str, **kwargs) -> str:
        """
        调用OpenAI API

        参数:
            config: 模型配置
            prompt: 提示词
            model: 模型名称
            **kwargs: 额外参数

        返回:
            模型响应

        异常:
            LLMError: 如果调用失败
        """
        url = f"{config['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000),
            "top_p": kwargs.get("top_p", 1.0)
        }

        try:
            response = self.session.post(
                url,
                headers=headers,
                json=data,
                timeout=config.get("timeout", 30)
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMError(f"OpenAI API调用失败: {str(e)}")

    def call_anthropic(self, config: Dict[str, Any], prompt: str, model: str, **kwargs) -> str:
        """
        调用Anthropic API

        参数:
            config: 模型配置
            prompt: 提示词
            model: 模型名称
            **kwargs: 额外参数

        返回:
            模型响应

        异常:
            LLMError: 如果调用失败
        """
        url = f"{config['base_url']}/messages"
        headers = {
            "x-api-key": config['api_key'],
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }

        try:
            response = self.session.post(
                url,
                headers=headers,
                json=data,
                timeout=config.get("timeout", 30)
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except Exception as e:
            raise LLMError(f"Anthropic API调用失败: {str(e)}")

    def call_gemini(self, config: Dict[str, Any], prompt: str, model: str, **kwargs) -> str:
        """
        调用Google Gemini API

        参数:
            config: 模型配置
            prompt: 提示词
            model: 模型名称
            **kwargs: 额外参数

        返回:
            模型响应

        异常:
            LLMError: 如果调用失败
        """
        url = f"{config['base_url']}/models/{model}:generateContent"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": config['api_key']
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 1000)
            }
        }

        try:
            response = self.session.post(
                url,
                headers=headers,
                params=params,
                json=data,
                timeout=config.get("timeout", 30)
            )
            response.raise_for_status()
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise LLMError(f"Gemini API调用失败: {str(e)}")

    def call_local_model(self, config: Dict[str, Any], prompt: str, model: str, **kwargs) -> str:
        """
        调用本地模型API

        参数:
            config: 模型配置
            prompt: 提示词
            model: 模型名称
            **kwargs: 额外参数

        返回:
            模型响应

        异常:
            LLMError: 如果调用失败
        """
        # 假设本地模型使用OpenAI兼容的API
        return self.call_openai(config, prompt, model, **kwargs)

    def call_deepseek(self, config: Dict[str, Any], prompt: str, model: str, **kwargs) -> str:
        """
        调用DeepSeek API

        参数:
            config: 模型配置
            prompt: 提示词
            model: 模型名称
            **kwargs: 额外参数

        返回:
            模型响应

        异常:
            LLMError: 如果调用失败
        """
        # DeepSeek API兼容OpenAI格式
        return self.call_openai(config, prompt, model, **kwargs)

    def call(self, prompt: str, provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> str:
        """
        调用LLM模型的统一接口

        参数:
            prompt: 提示词
            provider: 模型提供商名称，如果为None则使用默认提供商
            model: 模型名称，如果为None则使用默认模型
            **kwargs: 额外参数

        返回:
            模型响应

        异常:
            LLMError: 如果调用失败
        """
        # 获取模型配置
        config = self.get_model_config(provider)
        provider_name = provider or self.config_manager.get_default_provider()

        # 获取模型名称
        if model is None:
            model = self.config_manager.get_default_model()
            # 检查模型是否在提供商的模型列表中
            if model not in config.get("models", []):
                # 使用提供商的第一个模型
                model = config.get("models", [])[0]

        # 根据提供商调用相应的方法
        call_methods = {
            "openai": self.call_openai,
            "openai_proxy": self.call_openai,
            "anthropic": self.call_anthropic,
            "gemini": self.call_gemini,
            "local_model": self.call_local_model,
            "deepseek": self.call_deepseek
        }

        call_method = call_methods.get(provider_name)
        if not call_method:
            raise LLMError(f"不支持的模型提供商: {provider_name}")

        # 重试机制
        max_retries = config.get("max_retries", 3)
        for attempt in range(max_retries):
            try:
                return call_method(config, prompt, model, **kwargs)
            except LLMError as e:
                if attempt == max_retries - 1:
                    raise
                print(f"第 {attempt + 1} 次调用失败，重试中...: {str(e)}")

    def get_available_providers(self) -> List[str]:
        """
        获取所有可用的模型提供商

        返回:
            模型提供商名称列表
        """
        all_models = self.config_manager.get_all_models()
        return list(all_models.keys())

    def get_available_models(self, provider: Optional[str] = None) -> List[str]:
        """
        获取指定提供商的可用模型

        参数:
            provider: 模型提供商名称，如果为None则使用默认提供商

        返回:
            模型名称列表

        异常:
            LLMError: 如果提供商不存在
        """
        config = self.get_model_config(provider)
        return config.get("models", [])


# 全局LLM管理器实例
_llm_manager = None


def get_llm_manager() -> LLMManager:
    """
    获取全局LLM管理器实例

    返回:
        LLM管理器实例
    """
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager


# 便捷函数
def call_llm(prompt: str, provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> str:
    """
    便捷调用LLM模型的函数

    参数:
        prompt: 提示词
        provider: 模型提供商名称，如果为None则使用默认提供商
        model: 模型名称，如果为None则使用默认模型
        **kwargs: 额外参数

    返回:
        模型响应

    异常:
        LLMError: 如果调用失败
    """
    return get_llm_manager().call(prompt, provider, model, **kwargs)


def get_available_llm_providers() -> List[str]:
    """
    获取所有可用的LLM提供商

    返回:
        提供商名称列表
    """
    return get_llm_manager().get_available_providers()


def get_available_llm_models(provider: Optional[str] = None) -> List[str]:
    """
    获取指定提供商的可用模型

    参数:
        provider: 提供商名称，如果为None则使用默认提供商

    返回:
        模型名称列表
    """
    return get_llm_manager().get_available_models(provider)
