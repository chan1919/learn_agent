import os
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    """
    配置管理器
    用于读取和管理大模型接口配置
    """

    def __init__(self, config_path: str = None):
        """
        初始化配置管理器

        参数:
            config_path: 配置文件路径，默认使用config/config.yaml
        """
        if config_path is None:
            # 默认配置文件路径
            self.config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "config.yaml"
            )
        else:
            self.config_path = config_path

        self.config = None
        self._load_config()

    def _load_config(self):
        """
        加载配置文件
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            print(f"配置文件加载成功: {self.config_path}")
        except FileNotFoundError:
            print(f"错误: 配置文件不存在 - {self.config_path}")
            self.config = {}
        except yaml.YAMLError as e:
            print(f"错误: 配置文件格式错误 - {e}")
            self.config = {}

    def get_config(self) -> Dict[str, Any]:
        """
        获取完整配置

        返回:
            完整配置字典
        """
        return self.config

    def get_model_config(self, provider: str) -> Optional[Dict[str, Any]]:
        """
        获取指定模型提供商的配置

        参数:
            provider: 模型提供商名称

        返回:
            模型配置字典，如果不存在则返回None
        """
        if not self.config or 'models' not in self.config:
            return None

        return self.config['models'].get(provider)

    def get_all_models(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有模型配置

        返回:
            所有模型配置字典
        """
        if not self.config or 'models' not in self.config:
            return {}

        return self.config['models']

    def get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置

        返回:
            默认配置字典
        """
        if not self.config or 'defaults' not in self.config:
            return {}

        return self.config['defaults']

    def get_default_provider(self) -> str:
        """
        获取默认模型提供商

        返回:
            默认模型提供商名称
        """
        defaults = self.get_default_config()
        return defaults.get('model_provider', 'openai')

    def get_default_model(self) -> str:
        """
        获取默认模型

        返回:
            默认模型名称
        """
        defaults = self.get_default_config()
        return defaults.get('default_model', 'gpt-4o')

    def update_config(self, new_config: Dict[str, Any]):
        """
        更新配置

        参数:
            new_config: 新的配置字典
        """
        self.config.update(new_config)

    def save_config(self):
        """
        保存配置到文件
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            print(f"配置文件保存成功: {self.config_path}")
        except Exception as e:
            print(f"错误: 保存配置文件失败 - {e}")

    def validate_config(self) -> bool:
        """
        验证配置是否有效

        返回:
            配置是否有效的布尔值
        """
        if not self.config:
            return False

        # 检查必要的配置项
        required_fields = ['version', 'models', 'defaults']
        for field in required_fields:
            if field not in self.config:
                print(f"错误: 配置缺少必要字段 - {field}")
                return False

        # 检查模型配置
        if not isinstance(self.config['models'], dict):
            print("错误: 模型配置格式错误")
            return False

        return True

# 全局配置管理器实例
_config_manager = None

def get_config_manager() -> ConfigManager:
    """
    获取全局配置管理器实例

    返回:
        配置管理器实例
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager