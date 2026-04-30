"""
Jinja2 模板引擎封装
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from pathlib import Path
from typing import Dict, Any

try:
    from .utils import (
        to_snake_case, to_camel_case, to_pascal_case, to_kebab_case,
        pluralize, singularize, get_templates_dir, setup_logger
    )
except ImportError:
    from utils import (
        to_snake_case, to_camel_case, to_pascal_case, to_kebab_case,
        pluralize, singularize, get_templates_dir, setup_logger
    )

logger = setup_logger(__name__)


class TemplateEngine:
    """Jinja2 模板引擎封装"""

    def __init__(self, tech_stack: str = "react-fastapi"):
        """
        初始化模板引擎

        Args:
            tech_stack: 技术栈名称（如 "react-fastapi"）
        """
        self.tech_stack = tech_stack
        self.templates_root = get_templates_dir()
        self.tech_stack_dir = self.templates_root / tech_stack

        if not self.tech_stack_dir.exists():
            raise FileNotFoundError(
                f"技术栈模板目录不存在: {self.tech_stack_dir}"
            )

        # 创建 Jinja2 环境
        self.env = Environment(
            loader=FileSystemLoader(str(self.tech_stack_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # 注册自定义过滤器
        self.env.filters['snake_case'] = to_snake_case
        self.env.filters['camel_case'] = to_camel_case
        self.env.filters['pascal_case'] = to_pascal_case
        self.env.filters['kebab_case'] = to_kebab_case
        self.env.filters['pluralize'] = pluralize
        self.env.filters['singularize'] = singularize

        logger.info(f"模板引擎已初始化，技术栈: {tech_stack}")

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        渲染模板

        Args:
            template_name: 模板文件名（相对于技术栈目录）
            context: 模板上下文数据

        Returns:
            渲染后的字符串

        Raises:
            TemplateNotFound: 模板文件不存在
            Exception: 模板渲染失败
        """
        try:
            template = self.env.get_template(template_name)
            logger.debug(f"渲染模板: {template_name}")
            return template.render(**context)
        except TemplateNotFound as e:
            logger.error(f"模板不存在: {template_name}")
            raise
        except Exception as e:
            logger.error(f"模板渲染失败: {template_name}, 错误: {str(e)}")
            raise

    def render_to_file(
        self,
        template_name: str,
        context: Dict[str, Any],
        output_path: str
    ) -> None:
        """
        渲染模板并写入文件

        Args:
            template_name: 模板文件名
            context: 模板上下文数据
            output_path: 输出文件路径
        """
        content = self.render(template_name, context)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"文件已生成: {output_path}")

    def list_templates(self) -> list:
        """
        列出所有可用的模板

        Returns:
            模板文件名列表
        """
        templates = []
        for file_path in self.tech_stack_dir.rglob('*.j2'):
            relative_path = file_path.relative_to(self.tech_stack_dir)
            templates.append(str(relative_path))
        return templates

    def validate_context(self, template_name: str, context: Dict[str, Any]) -> bool:
        """
        验证上下文是否包含模板所需的所有变量

        Args:
            template_name: 模板文件名
            context: 上下文数据

        Returns:
            是否有效

        Note:
            这是一个简单的实现，只检查模板是否存在
            完整的实现需要解析模板文件提取变量
        """
        try:
            self.env.get_template(template_name)
            return True
        except TemplateNotFound:
            return False
