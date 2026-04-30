---
name: idea2web
description: "从一句话想法生成理想汽车风格的全栈Web应用(React+FastAPI+SQLite)。触发：用户想创建/构建/生成网页应用、网站、工具、仪表盘、CRUD应用或交互式网页项目。短语「我想做/构建/创建一个...」「帮我做...」「生成一个...应用/系统/工具」或描述软件想法时触发。自动处理前后端、数据库、CORS、部署脚本。不适用于WebSocket实时通信、视频音频处理、ML集成、第三方支付、复杂RBAC。"
---

# idea2web — 全栈 Web 应用生成器

将用户模糊想法转化为可运行的全栈应用，遵循四阶段流程：

1. **需求澄清** → 结构化 PRD
2. **架构规划** → API 契约 + 文件结构
3. **代码生成** → 用 Write 工具逐文件生成
4. **部署交付** → 启动脚本 + 使用指南

## 核心原则

- **固执己见**：不问用户选框架，自动选最优方案
- **完整代码**：禁止 `// TODO`、`// ...rest`、`# ...` 等占位符
- **理想汽车风格**：深色主题 + 香槟金强调色（见 [references/theme.md](references/theme.md)）
- **新手友好**：零配置、一键启动、含测试数据

## 支持的应用类型

✅ CRUD 应用、数据仪表盘、CMS、任务管理、用户管理后台、数据收集工具、商品目录
❌ WebSocket 实时通信、视频/音频处理、ML 集成、第三方支付、复杂 RBAC

超出范围时：告知用户并提供简化替代方案（如实时聊天 → 定期刷新留言板）。

## 技术栈选择

| 条件 | 栈 |
|---|---|
| 默认 | React (Vite) + FastAPI + SQLite + Tailwind |
| 用户提到 "Vue" | Vue 3 + FastAPI + SQLite + Element Plus |
| 用户说 "最简单" 或 "数据分析" | Streamlit + SQLite |

告知用户选择结果，不征求意见。

## 四阶段工作流

### 阶段 1：需求澄清

1. 从描述中提取**实体**（名词）和**操作**（动词）
2. 提出 **3-5 个**引导性问题（不超过 5 个），覆盖：用户范围、数据操作、视觉需求、导入/导出
3. 如果核心功能 > 5 个，建议用户**裁剪到 5 个**并列出优先级
4. 生成 `{app-name}-prd.json`，向用户确认后继续

PRD 格式见 [references/data-formats.md](references/data-formats.md)。

### 阶段 2：架构规划

1. 选择技术栈（见上表）
2. 设计数据库模式（SQLite，自增 id 主键）
3. 设计 RESTful API（所有端点 `/api/` 前缀，标准 CRUD 模式）
4. 生成 `api_spec.json`（OpenAPI 3.0）和 `file_tree.json`
5. 向用户展示方案，确认后继续

API 设计规范见 [references/data-formats.md](references/data-formats.md)。

### 阶段 3：代码生成

**关键：永远不要在对话中输出代码，始终使用 Write 工具直接创建文件。**

严格按顺序生成：

1. 文档：README.md, api_spec.json, PRD, file_tree.json
2. 后端：requirements.txt → database.py → models.py → routes.py → main.py → seed.py
3. 前端：package.json → vite.config.js → index.html → tailwind.config.js → **postcss.config.js** ⚠️ → index.css → api/client.js → App.jsx → main.jsx → 页面组件
4. 部署：start.py, start.bat, stop.bat, .gitignore

每 5-7 个文件输出进度：`✅ backend/app/main.py 已创建 📊 进度：[8/24]`

关键配置模式和代码模板见 [references/code-patterns.md](references/code-patterns.md)。
理想汽车 UI 风格规范见 [references/theme.md](references/theme.md)。

#### ⚠️ postcss.config.js 必须创建

没有此文件 Tailwind CSS 不工作，页面显示为无样式。

```javascript
export default {
  plugins: { tailwindcss: {}, autoprefixer: {} }
}
```

#### seed.py 测试数据

每个实体生成 8-10 条真实测试记录，防止"空白 UI"问题。支持 `--force` 重置。

### 阶段 4：部署交付

生成启动脚本和使用指南（**不自动启动**，让用户控制）：

- `start.bat` / `stop.bat` — Windows 一键启动/停止
- `start.py` — 跨平台 Python 启动脚本
- `新手使用指南.md` — 3 步快速开始
- `创建桌面快捷方式.md`

最终向用户展示：项目位置、启动方式、测试账号（如有）。

部署详情见 [references/deployment.md](references/deployment.md)。

## 文件生成验证清单

生成完毕后必须验证：

**前端：**
- ✅ `frontend/postcss.config.js` — **最常遗漏！**
- ✅ `frontend/tailwind.config.js` — 含理想汽车配色
- ✅ `frontend/vite.config.js` — 含 `/api` proxy 到 localhost:8000
- ✅ `frontend/src/index.css` — 含 `@tailwind` 指令和全局样式

**后端：**
- ✅ `backend/app/main.py` — 含 CORS（allow_origins 含 localhost:5173）
- ✅ `backend/seed.py` — 测试数据

## 错误处理

- 用户报错时：**先要错误信息**，不猜测
- 读取相关文件了解状态
- 用 Edit 工具修复，不重新生成整个文件
- 解释原因并教学

## 模板系统

本 skill 包含 Jinja2 模板（`templates/react-fastapi/`），可通过脚本渲染：

```bash
python scripts/generator.py quick --user-input "描述" --output-dir ./my-app
```

详见 [references/scripts-guide.md](references/scripts-guide.md)。
