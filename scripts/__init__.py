"""
idea2web - 全栈网页应用生成器

从用户描述生成完整的、可用于生产环境的全栈网页应用。
"""

__version__ = "1.0.0"
__author__ = "Claude"

from .generator import main
from .requirement_analyzer import RequirementAnalyzer
from .architecture_planner import ArchitecturePlanner
from .code_generator import CodeGenerator
from .template_engine import TemplateEngine
from .deployment_manager import DeploymentManager
from .config_manager import ConfigManager

__all__ = [
    "main",
    "RequirementAnalyzer",
    "ArchitecturePlanner",
    "CodeGenerator",
    "TemplateEngine",
    "DeploymentManager",
    "ConfigManager",
]
