"""
配置管理模块
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from .utils import get_config_dir, read_json_file, setup_logger
except ImportError:
    from utils import get_config_dir, read_json_file, setup_logger


logger = setup_logger(__name__)


class ConfigManager:
    """配置管理器"""

    def __init__(self):
        """初始化配置管理器"""
        self.config_dir = get_config_dir()
        self._default_config: Optional[Dict[str, Any]] = None
        self._tech_stacks: Optional[Dict[str, Any]] = None
        self._theme_presets: Optional[Dict[str, Any]] = None
        self._generation_order: Optional[Dict[str, Any]] = None

    @property
    def default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        if self._default_config is None:
            self._default_config = self._load_config('default_config.json')
        return self._default_config

    @property
    def tech_stacks(self) -> Dict[str, Any]:
        """获取技术栈配置"""
        if self._tech_stacks is None:
            self._tech_stacks = self._load_config('tech_stacks.json')
        return self._tech_stacks

    @property
    def theme_presets(self) -> Dict[str, Any]:
        """获取主题预设配置"""
        if self._theme_presets is None:
            self._theme_presets = self._load_config('theme_presets.json')
        return self._theme_presets

    @property
    def generation_order(self) -> Dict[str, Any]:
        """获取文件生成顺序配置"""
        if self._generation_order is None:
            self._generation_order = self._load_config('generation_order.json')
        return self._generation_order

    # Fallback defaults when config files are missing
    _FALLBACK_CONFIGS: Dict[str, Dict[str, Any]] = {
        'default_config.json': {
            'default_tech_stack': 'react-fastapi',
            'default_theme': 'li-auto',
            'max_features': 5,
            'ports': {'backend': 8000, 'frontend': 5173},
            'deployment': {
                'auto_start': False,
                'mirrors': {
                    'pip': 'https://pypi.tuna.tsinghua.edu.cn/simple',
                    'npm': 'https://registry.npmmirror.com'
                }
            }
        },
        'tech_stacks.json': {
            'react-fastapi': {
                'name': 'React + FastAPI',
                'frontend': 'react',
                'backend': 'fastapi',
                'database': 'sqlite'
            }
        },
        'theme_presets.json': {
            'li-auto': {'name': '理想汽车'}
        },
        'generation_order.json': {'phases': []}
    }

    def _load_config(self, filename: str) -> Dict[str, Any]:
        """
        加载配置文件，缺失时使用内置默认值。

        Args:
            filename: 配置文件名

        Returns:
            配置数据
        """
        config_path = self.config_dir / filename
        if not config_path.exists():
            fallback = self._FALLBACK_CONFIGS.get(filename)
            if fallback is not None:
                logger.warning(f"配置文件不存在: {config_path}，使用内置默认值")
                return fallback
            logger.error(f"配置文件不存在且无默认值: {config_path}")
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        logger.debug(f"加载配置文件: {filename}")
        try:
            return read_json_file(str(config_path))
        except Exception as e:
            fallback = self._FALLBACK_CONFIGS.get(filename)
            if fallback is not None:
                logger.warning(f"配置文件读取失败: {e}，使用内置默认值")
                return fallback
            raise

    def get_tech_stack(self, name: str) -> Dict[str, Any]:
        """
        获取指定技术栈的配置

        Args:
            name: 技术栈名称（如 "react-fastapi"）

        Returns:
            技术栈配置

        Raises:
            KeyError: 技术栈不存在
        """
        if name not in self.tech_stacks:
            available = ", ".join(self.tech_stacks.keys())
            raise KeyError(f"技术栈 '{name}' 不存在。可用的技术栈: {available}")

        return self.tech_stacks[name]

    def get_theme_preset(self, name: str) -> Dict[str, Any]:
        """
        获取指定主题预设的配置

        Args:
            name: 主题名称（如 "li-auto"）

        Returns:
            主题配置

        Raises:
            KeyError: 主题不存在
        """
        if name not in self.theme_presets:
            available = ", ".join(self.theme_presets.keys())
            raise KeyError(f"主题 '{name}' 不存在。可用的主题: {available}")

        return self.theme_presets[name]

    def get_default_ports(self) -> Dict[str, int]:
        """
        获取默认端口配置

        Returns:
            包含 backend 和 frontend 端口的字典
        """
        return self.default_config.get('ports', {
            'backend': 8000,
            'frontend': 5173
        })

    def get_mirrors(self) -> Dict[str, str]:
        """
        获取镜像源配置

        Returns:
            包含 pip 和 npm 镜像源的字典
        """
        return self.default_config.get('deployment', {}).get('mirrors', {
            'pip': 'https://pypi.tuna.tsinghua.edu.cn/simple',
            'npm': 'https://registry.npmmirror.com'
        })

    def get_max_features(self) -> int:
        """
        获取最大功能数量限制

        Returns:
            最大功能数
        """
        return self.default_config.get('max_features', 5)

    def should_auto_start(self) -> bool:
        """
        是否自动启动应用

        Returns:
            是否自动启动
        """
        return self.default_config.get('deployment', {}).get('auto_start', False)
