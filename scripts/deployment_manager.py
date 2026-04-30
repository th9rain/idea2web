"""
部署管理器 - 阶段4：部署管理（简化版）

负责环境检测和基本部署指导
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Tuple

try:
    from .utils import setup_logger
except ImportError:
    from utils import setup_logger


logger = setup_logger(__name__)


class DeploymentManager:
    """部署管理器"""

    def __init__(self, project_dir: str):
        """
        初始化部署管理器

        Args:
            project_dir: 项目目录
        """
        self.project_dir = Path(project_dir)
        self.backend_dir = self.project_dir / "backend"
        self.frontend_dir = self.project_dir / "frontend"

    def load_ports(self) -> Tuple[int, int]:
        """从 ports.json 加载端口配置"""
        ports_file = self.project_dir / "ports.json"
        if ports_file.exists():
            import json
            with open(ports_file, 'r') as f:
                ports = json.load(f)
                backend_port = ports.get('backend_port', 8000)
                frontend_port = ports.get('frontend_port', 5173)
            logger.info(f"使用分配的端口: 后端 {backend_port}, 前端 {frontend_port}")
            return backend_port, frontend_port
        # 如果 ports.json 不存在，返回默认端口
        logger.warning("ports.json 不存在，使用默认端口")
        return 8000, 5173

    def check_environment(self) -> Dict[str, bool]:
        """
        检查环境

        Returns:
            环境状态字典
        """
        logger.info("检查环境...")

        env_status = {
            'python': self._check_command("python", "--version"),
            'node': self._check_command("node", "--version"),
            'npm': self._check_command("npm", "--version"),
        }

        for tool, available in env_status.items():
            if available:
                logger.info(f"✅ {tool} 已安装")
            else:
                logger.warning(f"❌ {tool} 未安装")

        return env_status

    def _check_command(self, command: str, *args) -> bool:
        """检查命令是否可用"""
        try:
            result = subprocess.run(
                [command] + list(args),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
        except Exception as e:
            logger.debug(f"检查 {command} 失败: {e}")
            return False

    def print_deployment_instructions(self):
        """打印部署说明"""
        backend_port, frontend_port = self.load_ports()

        sep = '=' * 60
        activate_cmd = 'venv\\Scripts\\activate' if sys.platform == 'win32' else 'source venv/bin/activate'
        instructions = f"""
{sep}
部署说明
{sep}

项目已生成到：{self.project_dir}

已分配端口：后端 {backend_port}，前端 {frontend_port}
（端口配置保存在 ports.json 文件中）

请按以下步骤操作：

1. 安装后端依赖
   cd {self.backend_dir}
   python -m venv venv
   {activate_cmd}
   pip install -r requirements.txt

2. 初始化数据库
   python -c "from app.database import init_db; init_db()"

   (可选) 生成测试数据
   python seed.py

3. 安装前端依赖
   cd {self.frontend_dir}
   npm install

4. 启动应用
   # 方式1：使用启动脚本（推荐）
   cd {self.project_dir}
   python start.py

   # 方式2：手动启动
   # 终端1 - 后端
   cd {self.backend_dir}
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port {backend_port}

   # 终端2 - 前端
   cd {self.frontend_dir}
   npm run dev

5. 访问应用
   前端：http://localhost:{frontend_port}
   后端 API：http://localhost:{backend_port}
   API 文档：http://localhost:{backend_port}/docs

{sep}
"""
        print(instructions)
        logger.info("部署说明已生成")
