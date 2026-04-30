# 数据格式规范

## PRD 文件（{app-name}-prd.json）

```json
{
  "app_name": "应用名称",
  "description": "简要描述",
  "tech_stack": "react-fastapi",
  "features": [
    {
      "id": "feature_id",
      "name": "功能名称",
      "type": "form|list|detail|chart|export",
      "priority": "high|medium|low",
      "description": "此功能的作用",
      "ui_elements": ["输入字段", "按钮", "表格"],
      "data_flow": "用户操作 → API 调用 → 数据库 → 响应"
    }
  ],
  "data_entities": [
    {
      "name": "实体名称",
      "description": "此实体代表什么",
      "fields": {
        "field_name": {
          "type": "string|integer|float|boolean|datetime|text",
          "required": true,
          "description": "字段说明"
        }
      },
      "relationships": ["EntityName has many OtherEntity"]
    }
  ],
  "user_roles": ["admin", "user"],
  "auth_required": true
}
```

## API 契约（api_spec.json）

使用 OpenAPI 3.0 格式：

```json
{
  "openapi": "3.0.0",
  "info": { "title": "应用名称 API", "version": "1.0.0" },
  "servers": [{ "url": "http://localhost:8000" }],
  "paths": {
    "/api/{entities}": {
      "get": { "summary": "列出所有", "responses": { "200": { "description": "成功" } } },
      "post": { "summary": "创建", "responses": { "201": { "description": "已创建" } } }
    },
    "/api/{entities}/{id}": {
      "get": { "summary": "获取单个" },
      "put": { "summary": "更新" },
      "delete": { "summary": "删除" }
    }
  },
  "components": { "schemas": { /* Pydantic model 对应 */ } }
}
```

## RESTful API 设计规范

### 标准 CRUD

```
GET    /api/{entities}          → 列出所有（分页可选）
POST   /api/{entities}          → 创建
GET    /api/{entities}/{id}     → 获取单个
PUT    /api/{entities}/{id}     → 更新
DELETE /api/{entities}/{id}     → 删除
```

### 扩展端点（按需）

```
GET    /api/{entities}/search?q={query}   → 搜索
GET    /api/{entities}/stats              → 统计
POST   /api/{entities}/bulk               → 批量操作
GET    /api/health                        → 健康检查
```

## 文件结构计划（file_tree.json）

```json
{
  "project_root": "{app-name}",
  "files": [
    { "path": "backend/app/main.py", "purpose": "FastAPI 入口", "size_estimate": "medium" }
  ],
  "directory_structure": {
    "backend/app": ["__init__.py", "main.py", "models.py", "routes.py", "database.py"],
    "frontend/src": { "components": ["*.jsx"], "pages": ["*.jsx"], "api": ["client.js"] }
  }
}
```
