# idea2web

[English](README.md) | [简体中文](README.zh-CN.md)

> 把一个模糊的产品想法，落成一个可运行的全栈 Web 应用脚手架。

`idea2web` 是一个可复用的 Skill 和 CLI 工作流，用来把一句简短的产品描述整理成结构化方案，并生成一个可以直接继续开发的起始应用。

它面向的就是这段空白：从“我有个想法”到“我有个能跑、能看、能继续改的项目骨架”。

## 它能做什么

面对下面这种简短需求：
- “做一个内部 dashboard”
- “做一个任务管理 CRUD 工具”
- “生成一个审批用的小型运营应用”

`idea2web` 会帮助产出：
- 结构化需求澄清
- 轻量 PRD
- 架构和 API 规划
- 全栈项目脚手架
- 启动和交付说明

## 默认技术栈

当前最成熟的模板路径是这套务实的默认栈：
- React + Vite
- FastAPI
- SQLite
- Tailwind CSS

仓库结构允许以后扩展更多栈，但当前公开版本故意保持收敛，只把最能复用的一条路径做好。

## 工作流

`idea2web` 分成四个阶段：

1. **需求澄清**
   - 提取实体、操作和约束
   - 暴露缺失假设
   - 产出结构化 PRD

2. **架构规划**
   - 选择技术栈
   - 设计数据模型和 API
   - 产出实现计划和文件树

3. **代码生成**
   - 生成后端、前端、配置和 seed 资源
   - 把模板渲染成可运行脚手架

4. **交付**
   - 提供启动脚本
   - 提供面向初学者的使用说明

## 快速开始

先安装依赖：

```bash
pip install -r requirements.txt
```

一键生成项目：

```bash
python -m scripts quick --user-input "Build an internal task dashboard" --output-dir ./my-app
```

也可以按阶段执行：

```bash
python scripts/generator.py analyze --user-input "Build an internal task dashboard" --output prd.json
python scripts/generator.py plan --prd prd.json --output architecture.json
python scripts/generator.py generate --architecture architecture.json --output-dir ./my-app
```

## 仓库结构

```text
idea2web/
|-- README.md
|-- README.zh-CN.md
|-- LICENSE
|-- SKILL.md
|-- requirements.txt
|-- config/
|-- evals/
|-- references/
|-- scripts/
`-- templates/
```

## 关键文件

- `SKILL.md` - 面向 product-to-build 工作流的可复用 Skill 定义
- `scripts/` - CLI 入口和生成流水线
- `templates/react-fastapi/` - 当前默认技术栈对应的脚手架模板
- `config/` - 生成默认值、执行顺序和技术栈元信息
- `references/` - 实现说明、部署指导和生成规则
- `evals/` - 用于检查工作流质量的评测样例

## 这个仓库不是什么

这个仓库不是：
- 一个成品级 no-code 平台
- 一个覆盖所有前后端框架的通用网站生成器
- 一个已经产品化的 SaaS

它更适合作为一套可重复使用的“idea 到 runnable app”工作流起点。

## 为什么做这个仓库

很多产品想法死在“还没落成第一个可用版本”之前。

`idea2web` 想压缩的就是这段距离：
- 把模糊需求变成结构化信息
- 把结构变成实现决策
- 把决策变成一个真的能继续开发的起始代码库

## 当前限制

现在这个仓里最强的一条路径，就是 React + FastAPI 脚手架。这是有意为之。

对公开仓来说，一条清晰、可复用的主路径，通常比“看起来支持一切”更有说服力。

## 建议的 GitHub 元信息

**仓库描述**

> Turn product ideas into practical full-stack web app scaffolds.

**建议 topics**

```text
code-generation
full-stack
app-generator
fastapi
react
vite
tailwindcss
developer-tools
workflow-automation
```

## 相关主题

- reusable skills
- AI workflow systems
- product-to-build automation
- practical full-stack generation

## License

MIT
