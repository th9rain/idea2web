# 脚本与模板使用指南

## CLI 入口

```bash
# 快速生成（一步到位）
python scripts/generator.py quick --user-input "描述" --output-dir ./my-app

# 分步生成
python scripts/generator.py analyze --user-input "描述" --output prd.json
python scripts/generator.py plan --prd prd.json --output architecture.json
python scripts/generator.py generate --architecture architecture.json --output-dir ./my-app
python scripts/generator.py deploy --project-dir ./my-app
```

## 脚本清单

| 脚本 | 阶段 | 功能 |
|---|---|---|
| `generator.py` | 入口 | CLI 主入口，协调 4 阶段 |
| `requirement_analyzer.py` | 1 | 需求分析 → PRD |
| `architecture_planner.py` | 2 | 架构规划 → API 契约 |
| `code_generator.py` | 3 | Jinja2 模板渲染 → 代码 |
| `deployment_manager.py` | 4 | 环境检测 + 部署指导 |
| `template_engine.py` | 3 | Jinja2 模板引擎封装 |
| `config_manager.py` | 全局 | 配置文件读取管理 |
| `utils.py` | 全局 | 通用工具函数 |

## 模板系统

模板位于 `templates/react-fastapi/`，使用 Jinja2（.j2 扩展名）。

### 模板结构

```
templates/react-fastapi/
├── backend/     # 后端模板（7个）
│   ├── main.py.j2
│   ├── database.py.j2
│   ├── models.py.j2
│   ├── routes.py.j2
│   ├── requirements.txt.j2
│   ├── seed.py.j2
│   └── __init__.py.j2
├── frontend/    # 前端模板（9个）
│   ├── package.json.j2
│   ├── vite.config.js.j2
│   ├── index.html.j2
│   ├── tailwind.config.js.j2
│   ├── postcss.config.js.j2
│   ├── src/index.css.j2
│   ├── src/api/client.js.j2
│   ├── src/App.jsx.j2
│   └── src/main.jsx.j2
└── root/        # 根目录模板
    ├── start.py.j2
    ├── start.bat.j2
    ├── stop.bat.j2
    ├── check_and_fix.py.j2
    ├── wait_for_port.py.j2
    ├── .gitignore.j2
    ├── README.md.j2
    ├── 新手使用指南.md.j2
    └── 创建桌面快捷方式.md.j2
```

### 调试模板

```python
from scripts.template_engine import TemplateEngine

engine = TemplateEngine("react-fastapi")
content = engine.render("backend/main.py.j2", {
    'app_name': 'TestApp',
    # ... 其他上下文
})
print(content)
```

## 配置文件

| 文件 | 用途 |
|---|---|
| `config/default_config.json` | 默认技术栈、端口、镜像源等 |
| `config/tech_stacks.json` | 可用技术栈定义 |
| `config/theme_presets.json` | 主题预设（理想汽车等） |
| `config/generation_order.json` | 文件生成顺序定义 |

## Python 依赖

运行脚本需要安装：

```bash
pip install jinja2 pyyaml
```
