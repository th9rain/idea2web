"""
idea2web 主入口 CLI

命令行接口，协调 4 阶段流程
"""

import sys
import click
import json
from pathlib import Path
from typing import Optional

try:
    from .requirement_analyzer import RequirementAnalyzer, PRD
    from .architecture_planner import ArchitecturePlanner, Architecture
    from .code_generator import CodeGenerator
    from .template_engine import TemplateEngine
    from .deployment_manager import DeploymentManager
    from .config_manager import ConfigManager
    from .utils import setup_logger, write_json_file, read_json_file
except ImportError:
    from requirement_analyzer import RequirementAnalyzer, PRD
    from architecture_planner import ArchitecturePlanner, Architecture
    from code_generator import CodeGenerator
    from template_engine import TemplateEngine
    from deployment_manager import DeploymentManager
    from config_manager import ConfigManager
    from utils import setup_logger, write_json_file, read_json_file



logger = setup_logger("idea2web")


@click.group(invoke_without_command=True)
@click.version_option(version="1.0.0")
@click.pass_context
def cli(ctx):
    """idea2web - 全栈网页应用生成器

    从用户描述生成完整的全栈网页应用。

    快速开始:
      python scripts/generator.py quick --user-input "我想做一个记账软件" --output-dir ./my-app

    分步执行:
      python scripts/generator.py analyze --user-input "..." --output prd.json
      python scripts/generator.py plan --prd prd.json --output architecture.json
      python scripts/generator.py generate --architecture architecture.json --output-dir ./my-app

    依赖安装:
      pip install -r requirements.txt
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--user-input', required=True, help='用户需求描述')
@click.option('--output', default='prd.json', help='输出文件路径')
def analyze(user_input: str, output: str):
    """阶段1：需求分析"""
    logger.info("=" * 60)
    logger.info("阶段1：需求分析")
    logger.info("=" * 60)

    analyzer = RequirementAnalyzer()
    prd = analyzer.analyze(user_input)

    # 保存 PRD
    write_json_file(output, prd.model_dump())
    logger.info(f"PRD 已保存到: {output}")

    # 显示警告
    if prd.warnings:
        logger.warning("\n警告：")
        for warning in prd.warnings:
            logger.warning(f"  - {warning}")

    logger.info(f"\n应用名称: {prd.app_name}")
    logger.info(f"数据实体: {len(prd.data_entities)} 个")
    logger.info(f"功能需求: {len(prd.features)} 个")


@cli.command()
@click.option('--prd', required=True, help='PRD 文件路径')
@click.option('--tech-stack', default='react-fastapi', help='技术栈')
@click.option('--output', default='architecture.json', help='输出文件路径')
def plan(prd: str, tech_stack: str, output: str):
    """阶段2：架构规划"""
    logger.info("=" * 60)
    logger.info("阶段2：架构规划")
    logger.info("=" * 60)

    # 加载 PRD
    prd_data = read_json_file(prd)
    prd_obj = PRD(**prd_data)

    planner = ArchitecturePlanner(tech_stack)
    architecture = planner.plan(prd_obj)

    # 保存 Architecture
    write_json_file(output, architecture.model_dump())
    logger.info(f"Architecture 已保存到: {output}")

    logger.info(f"\n数据库表: {len(architecture.database_schema.tables)} 个")
    logger.info(f"API 端点: {len(architecture.api_endpoints)} 个")


@cli.command()
@click.option('--architecture', required=True, help='Architecture 文件路径')
@click.option('--output-dir', required=True, help='输出目录')
def generate(architecture: str, output_dir: str):
    """阶段3：代码生成"""
    logger.info("=" * 60)
    logger.info("阶段3：代码生成")
    logger.info("=" * 60)

    # 加载 Architecture
    arch_data = read_json_file(architecture)
    arch_obj = Architecture(**arch_data)

    # 创建模板引擎和代码生成器
    template_engine = TemplateEngine(arch_obj.tech_stack)
    code_gen = CodeGenerator(template_engine)

    # 生成代码
    report = code_gen.generate(arch_obj, output_dir)

    logger.info(f"\n✅ {report.summary()}")
    logger.info(f"项目已生成到: {output_dir}")


@cli.command()
@click.option('--project-dir', required=True, help='项目目录')
def deploy(project_dir: str):
    """阶段4：部署管理"""
    logger.info("=" * 60)
    logger.info("阶段4：部署管理")
    logger.info("=" * 60)

    deployment = DeploymentManager(project_dir)

    # 检查环境
    env_status = deployment.check_environment()

    # 显示部署说明
    deployment.print_deployment_instructions()


@cli.command()
@click.option('--user-input', required=True, help='用户需求描述')
@click.option('--output-dir', required=True, help='输出目录')
@click.option('--tech-stack', default='react-fastapi', help='技术栈')
def quick(user_input: str, output_dir: str, tech_stack: str):
    """快速生成（跳过交互，一键完成所有阶段）"""
    logger.info("=" * 60)
    logger.info("idea2web 快速生成")
    logger.info("=" * 60)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 阶段1：需求分析
    logger.info("\n阶段1：需求分析")
    analyzer = RequirementAnalyzer()
    prd = analyzer.analyze(user_input)
    prd_file = output_path / "prd.json"
    write_json_file(str(prd_file), prd.model_dump())
    logger.info(f"✅ PRD 已保存: {prd_file}")

    # 阶段2：架构规划
    logger.info("\n阶段2：架构规划")
    planner = ArchitecturePlanner(tech_stack)
    architecture = planner.plan(prd)
    arch_file = output_path / "architecture.json"
    write_json_file(str(arch_file), architecture.model_dump())
    logger.info(f"✅ Architecture 已保存: {arch_file}")

    # 阶段3：代码生成
    logger.info("\n阶段3：代码生成")
    template_engine = TemplateEngine(tech_stack)
    code_gen = CodeGenerator(template_engine)
    report = code_gen.generate(architecture, output_dir)
    logger.info(f"✅ {report.summary()}")

    # 阶段4：部署说明
    logger.info("\n阶段4：部署说明")
    deployment = DeploymentManager(output_dir)
    deployment.check_environment()
    deployment.print_deployment_instructions()


@cli.command()
def info():
    """显示技能信息"""
    info_text = """
idea2web - 全栈网页应用生成器

从用户描述生成完整的、可用于生产环境的全栈网页应用。

支持的技术栈：
  - React + FastAPI（默认）

支持的应用类型：
  ✅ CRUD 应用
  ✅ 数据仪表盘
  ✅ 任务管理工具
  ✅ 用户管理系统

使用方法：
  # 快速生成（推荐）
  python generator.py quick --user-input "我想做一个记账软件" --output-dir ./my-app

  # 分步生成
  python generator.py analyze --user-input "..." --output prd.json
  python generator.py plan --prd prd.json --output architecture.json
  python generator.py generate --architecture architecture.json --output-dir ./my-app
  python generator.py deploy --project-dir ./my-app

更多信息：https://github.com/anthropics/claude-code
"""
    print(info_text)


def main():
    """主函数"""
    try:
        cli()
    except Exception as e:
        logger.error(f"执行失败: {e}")
        logger.error("请检查配置文件和依赖是否完整。")
        logger.error("运行 'pip install -r requirements.txt' 安装依赖。")
        sys.exit(1)


if __name__ == '__main__':
    # When run directly, ensure scripts dir is on path
    import os
    _dir = os.path.dirname(os.path.abspath(__file__))
    if _dir not in sys.path:
        sys.path.insert(0, _dir)
    try:
        main()
    except ImportError as e:
        print(f"错误: 缺少依赖 — {e}", file=sys.stderr)
        print("请运行: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
