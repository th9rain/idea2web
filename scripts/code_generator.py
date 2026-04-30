"""
代码生成器 - 阶段3：代码生成

使用 Jinja2 模板渲染生成完整项目代码
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple

try:
    from .architecture_planner import Architecture
    from .template_engine import TemplateEngine
    from .config_manager import ConfigManager
    from .utils import setup_logger, ensure_dir, write_json_file, allocate_ports
except ImportError:
    from architecture_planner import Architecture
    from template_engine import TemplateEngine
    from config_manager import ConfigManager
    from utils import setup_logger, ensure_dir, write_json_file, allocate_ports


logger = setup_logger(__name__)


class GenerationReport:
    """代码生成报告"""

    def __init__(self):
        self.files_generated = []
        self.total_lines = 0
        self.backend_port = 8000
        self.frontend_port = 5173

    def add_file(self, file_path: str, line_count: int):
        """添加生成的文件"""
        self.files_generated.append({
            'path': file_path,
            'lines': line_count
        })
        self.total_lines += line_count

    def set_ports(self, backend_port: int, frontend_port: int):
        """设置端口信息"""
        self.backend_port = backend_port
        self.frontend_port = frontend_port

    def summary(self) -> str:
        """生成摘要"""
        return (
            f"已生成 {len(self.files_generated)} 个文件，共 {self.total_lines} 行代码\n"
            f"后端端口: {self.backend_port}, 前端端口: {self.frontend_port}"
        )


class CodeGenerator:
    """代码生成器"""

    def __init__(
        self,
        template_engine: TemplateEngine,
        config_manager: ConfigManager = None
    ):
        """
        初始化代码生成器

        Args:
            template_engine: 模板引擎
            config_manager: 配置管理器（可选）
        """
        self.template = template_engine
        self.config = config_manager or ConfigManager()
        self.generation_order = self.config.generation_order

    def generate(self, architecture: Architecture, output_dir: str) -> GenerationReport:
        """
        生成所有代码文件

        Args:
            architecture: 架构设计
            output_dir: 输出目录

        Returns:
            GenerationReport 生成报告
        """
        logger.info(f"开始代码生成，输出目录: {output_dir}")

        output_path = Path(output_dir)
        ensure_dir(output_path)

        report = GenerationReport()

        # 动态分配端口
        logger.info("检测可用端口...")
        backend_port, frontend_port = allocate_ports()
        report.set_ports(backend_port, frontend_port)
        logger.info(f"✅ 使用端口: 后端 {backend_port}, 前端 {frontend_port}")

        # 准备全局上下文
        global_context = self._prepare_global_context(architecture, backend_port, frontend_port)

        # 按阶段生成文件
        for phase in self.generation_order['phases']:
            logger.info(f"阶段 {phase['order']}: {phase['name']}")

            for file_spec in phase['files']:
                file_path = output_path / file_spec['path']
                template_name = file_spec['template']

                try:
                    # 准备文件特定上下文
                    context = self._prepare_file_context(
                        global_context,
                        file_spec,
                        architecture
                    )

                    # 渲染模板
                    content = self.template.render(template_name, context)

                    # 写入文件
                    self._write_file(file_path, content)

                    # 统计行数
                    line_count = len(content.splitlines())
                    report.add_file(str(file_path), line_count)

                    logger.debug(f"✅ {file_spec['path']} ({line_count} 行)")

                except Exception as e:
                    logger.error(f"❌ 生成失败: {file_spec['path']}, 错误: {str(e)}")
                    raise

        # 保存端口配置到 ports.json
        self._save_ports_config(output_path, backend_port, frontend_port)

        # 更新 architecture.json 包含端口信息
        self._save_metadata(output_path, architecture, backend_port, frontend_port)

        # 验证关键文件是否生成
        self._verify_critical_files(output_path, global_context)

        logger.info(f"代码生成完成：{report.summary()}")
        return report

    def _prepare_global_context(
        self,
        arch: Architecture,
        backend_port: int,
        frontend_port: int
    ) -> Dict[str, Any]:
        """准备全局上下文"""
        tech_stack_config = self.config.get_tech_stack(arch.tech_stack)
        theme_config = self.config.get_theme_preset(self.config.default_config['default_theme'])

        return {
            'app_name': arch.app_name,
            'tech_stack': tech_stack_config,
            'theme': theme_config,
            'database_schema': arch.database_schema,
            'api_endpoints': arch.api_endpoints,
            'description': "由 idea2web 生成的全栈应用",
            'backend_port': backend_port,
            'frontend_port': frontend_port,
        }

    def _prepare_file_context(
        self,
        global_context: Dict[str, Any],
        file_spec: Dict[str, Any],
        architecture: Architecture
    ) -> Dict[str, Any]:
        """准备文件特定上下文"""
        context = global_context.copy()

        # 根据文件类型添加特定上下文
        file_type = file_spec.get('type', '')

        if file_type == 'model':
            # 数据模型文件
            context['entities'] = architecture.database_schema.tables
        elif file_type == 'route':
            # 路由文件
            context['routes'] = architecture.api_endpoints
        elif file_type == 'component':
            # 前端组件
            context['pages'] = architecture.database_schema.tables

        return context

    def _write_file(self, file_path: Path, content: str):
        """写入文件"""
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _save_ports_config(self, output_path: Path, backend_port: int, frontend_port: int):
        """保存端口配置"""
        ports_file = output_path / "ports.json"
        write_json_file(
            str(ports_file),
            {
                'backend_port': backend_port,
                'frontend_port': frontend_port
            }
        )
        logger.debug(f"✅ ports.json 已保存: {backend_port}, {frontend_port}")

    def _save_metadata(
        self,
        output_path: Path,
        architecture: Architecture,
        backend_port: int,
        frontend_port: int
    ):
        """保存元数据"""
        # 保存 architecture.json
        arch_data = architecture.model_dump()
        arch_data['allocated_ports'] = {
            'backend': backend_port,
            'frontend': frontend_port
        }

        arch_file = output_path / "architecture.json"
        write_json_file(str(arch_file), arch_data)
        logger.debug(f"✅ architecture.json")

    def _verify_critical_files(self, output_path: Path, context: Dict[str, Any]):
        """
        验证关键文件是否生成

        如果关键文件缺失，尝试重新生成
        """
        critical_files = [
            {
                'path': 'frontend/postcss.config.js',
                'template': 'frontend/postcss.config.js.j2',
                'reason': '前端样式处理必需（Tailwind CSS依赖）'
            },
            {
                'path': 'frontend/tailwind.config.js',
                'template': 'frontend/tailwind.config.js.j2',
                'reason': 'Tailwind CSS配置必需'
            }
        ]

        missing_files = []

        for file_info in critical_files:
            file_path = output_path / file_info['path']
            if not file_path.exists():
                missing_files.append(file_info)
                logger.warning(f"⚠️  关键文件缺失: {file_info['path']} - {file_info['reason']}")

        # 如果有缺失的关键文件，尝试重新生成
        if missing_files:
            logger.info(f"📝 尝试重新生成 {len(missing_files)} 个缺失的关键文件...")

            for file_info in missing_files:
                try:
                    file_path = output_path / file_info['path']
                    template_name = file_info['template']

                    # 渲染模板
                    content = self.template.render(template_name, context)

                    # 写入文件
                    self._write_file(file_path, content)

                    logger.info(f"✅ 已重新生成: {file_info['path']}")

                except Exception as e:
                    logger.error(f"❌ 重新生成失败: {file_info['path']}, 错误: {str(e)}")
                    # 不抛出异常，继续处理其他文件

        # 最终验证
        final_check = []
        for file_info in critical_files:
            file_path = output_path / file_info['path']
            if not file_path.exists():
                final_check.append(file_info['path'])

        if final_check:
            error_msg = f"关键文件仍然缺失: {', '.join(final_check)}"
            logger.error(f"❌ {error_msg}")
            logger.error("这可能导致前端样式无法正确加载！")
            # 警告但不终止，让用户能看到问题
        else:
            logger.debug("✅ 所有关键文件验证通过")

