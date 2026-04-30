# 部署与交付

## 设计理念

- 生成启动脚本，**不自动启动**（让用户控制）
- Windows 用户优先（bat 文件支持）
- 新手友好（详细指南 + 错误提示）
- 沙盒化环境（Python venv + Node 项目隔离）

## 生成的部署文件

### start.bat（Windows 一键启动）

功能：
- 检查端口占用
- 验证 Python venv 和 node_modules
- 初始化数据库
- 独立窗口启动前后端
- 自动打开浏览器

### stop.bat（Windows 一键停止）

功能：
- 按端口查找并终止进程
- 关闭服务窗口

### start.py（跨平台 Python 启动）

跨平台支持 Windows/Mac/Linux：端口检查、依赖验证、服务启动。

### 新手使用指南.md

包含：3 步快速开始、停止方式、常见问题 FAQ、高级操作。

### 创建桌面快捷方式.md

包含：拖拽 / 右键两种创建方式。

## 最终输出信息模板

```
============================================================
✅ {app_name} 代码生成完成！
============================================================

📁 项目位置：{project_path}

🚀 启动方式（3选1）：
   1. [推荐] Windows：双击 start.bat
   2. 跨平台：python start.py
   3. 命令行：cd {project_path} && start.bat

🛑 停止方式：双击 stop.bat / 关闭服务窗口 / Ctrl+C

📖 使用指南：新手使用指南.md（推荐先看）

⚠️ 首次使用前请先安装依赖（详见使用指南第1步）

{如有认证: 🔑 测试账号: testuser / password123}
============================================================
```

## 环境要求

- Python 3.8+
- Node.js 16+
- npm

## 国内镜像

默认配置使用国内镜像加速：
- pip: `https://pypi.tuna.tsinghua.edu.cn/simple`
- npm: `https://registry.npmmirror.com`
