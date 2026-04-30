"""
架构规划器 - 阶段2：架构规划

根据 PRD 设计技术架构和 API 契约
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

try:
    from .requirement_analyzer import PRD, Entity
    from .utils import setup_logger, to_snake_case, pluralize
    from .config_manager import ConfigManager
except ImportError:
    from requirement_analyzer import PRD, Entity
    from utils import setup_logger, to_snake_case, pluralize
    from config_manager import ConfigManager


logger = setup_logger(__name__)


# ===== Pydantic 数据模型 =====

class DatabaseColumn(BaseModel):
    """数据库列定义"""
    name: str = Field(default="", description="列名")
    type: str = Field(default="TEXT", description="SQL 类型")
    nullable: bool = Field(default=True, description="是否可为空")
    primary_key: bool = Field(default=False, description="是否为主键")
    index: bool = Field(default=False, description="是否添加索引")


class DatabaseTable(BaseModel):
    """数据库表定义"""
    name: str = Field(default="", description="表名")
    columns: List[DatabaseColumn] = Field(default_factory=list, description="列定义")
    indexes: List[str] = Field(default_factory=list, description="索引列表")


class DatabaseSchema(BaseModel):
    """数据库模式"""
    tables: List[DatabaseTable] = Field(default_factory=list, description="表列表")


class APIEndpoint(BaseModel):
    """API 端点定义"""
    method: str = Field(default="GET", description="HTTP 方法：GET, POST, PUT, DELETE")
    path: str = Field(default="", description="路径：/api/items")
    description: str = Field(default="", description="端点描述")
    request_schema: str = Field(default="", description="请求 schema")
    response_schema: str = Field(default="", description="响应 schema")
    tags: List[str] = Field(default_factory=list, description="OpenAPI 标签")


class Architecture(BaseModel):
    """架构设计"""
    app_name: str = Field(default="", description="应用名称")
    tech_stack: str = Field(default="react-fastapi", description="技术栈")
    database_schema: DatabaseSchema = Field(default_factory=DatabaseSchema, description="数据库模式")
    api_endpoints: List[APIEndpoint] = Field(default_factory=list, description="API 端点列表")
    openapi_spec: Dict[str, Any] = Field(default_factory=dict, description="OpenAPI 3.0 规范")
    file_tree: Dict[str, Any] = Field(default_factory=dict, description="文件结构")


# ===== 架构规划器 =====

class ArchitecturePlanner:
    """架构规划器"""

    def __init__(
        self,
        tech_stack: str = "react-fastapi",
        config_manager: Optional[ConfigManager] = None
    ):
        """
        初始化架构规划器

        Args:
            tech_stack: 技术栈名称
            config_manager: 配置管理器（可选）
        """
        self.tech_stack = tech_stack
        self.config = config_manager or ConfigManager()
        self.stack_config = self.config.get_tech_stack(tech_stack)

        # SQL 类型映射
        self.type_mapping = {
            'string': 'String',
            'integer': 'Integer',
            'float': 'Float',
            'boolean': 'Boolean',
            'datetime': 'DateTime',
            'text': 'Text',
        }

    def plan(self, prd: PRD) -> Architecture:
        """
        根据 PRD 规划架构

        Args:
            prd: 产品需求文档

        Returns:
            Architecture 对象
        """
        logger.info("开始架构规划")

        # 设计数据库模式
        database_schema = self._design_database(prd.data_entities)

        # 设计 API 端点
        api_endpoints = self._design_api(prd.data_entities, prd.features)

        # 生成 OpenAPI 规范
        openapi_spec = self._generate_openapi(prd, api_endpoints)

        # 规划文件结构
        file_tree = self._plan_file_structure(prd)

        architecture = Architecture(
            app_name=prd.app_name,
            tech_stack=self.tech_stack,
            database_schema=database_schema,
            api_endpoints=api_endpoints,
            openapi_spec=openapi_spec,
            file_tree=file_tree
        )

        logger.info(f"架构规划完成：{len(database_schema.tables)} 个表，{len(api_endpoints)} 个端点")
        return architecture

    def _design_database(self, entities: List[Entity]) -> DatabaseSchema:
        """设计数据库模式"""
        tables = []

        for entity in entities:
            table_name = to_snake_case(pluralize(entity.name))

            # 添加主键列
            columns = [
                DatabaseColumn(
                    name="id",
                    type="Integer",
                    nullable=False,
                    primary_key=True,
                    index=True
                )
            ]

            # 添加实体字段列
            for field_name, field_spec in entity.fields.items():
                sql_type = self.type_mapping.get(field_spec.type, 'String')
                columns.append(
                    DatabaseColumn(
                        name=field_name,
                        type=sql_type,
                        nullable=not field_spec.required,
                        index=field_spec.required  # 必填字段添加索引
                    )
                )

            # 添加时间戳列
            columns.extend([
                DatabaseColumn(
                    name="created_at",
                    type="DateTime",
                    nullable=False
                ),
                DatabaseColumn(
                    name="updated_at",
                    type="DateTime",
                    nullable=False
                )
            ])

            # 创建表定义
            table = DatabaseTable(
                name=table_name,
                columns=columns,
                indexes=[col.name for col in columns if col.index and not col.primary_key]
            )
            tables.append(table)

        return DatabaseSchema(tables=tables)

    def _design_api(self, entities: List[Entity], features: List) -> List[APIEndpoint]:
        """设计 RESTful API 端点"""
        endpoints = []

        for entity in entities:
            entity_name = entity.name
            entity_lower = entity_name.lower()
            entity_plural = pluralize(entity_lower)
            base_path = f"/api/{entity_plural}"

            # 标准 CRUD 端点
            endpoints.extend([
                # GET /api/items - 列出所有
                APIEndpoint(
                    method="GET",
                    path=base_path,
                    description=f"列出所有 {entity_name}",
                    response_schema=f"List[{entity_name}]",
                    tags=[entity_name]
                ),
                # POST /api/items - 创建新的
                APIEndpoint(
                    method="POST",
                    path=base_path,
                    description=f"创建新的 {entity_name}",
                    request_schema=f"{entity_name}Create",
                    response_schema=entity_name,
                    tags=[entity_name]
                ),
                # GET /api/items/{id} - 获取单个
                APIEndpoint(
                    method="GET",
                    path=f"{base_path}/{{id}}",
                    description=f"获取单个 {entity_name}",
                    response_schema=entity_name,
                    tags=[entity_name]
                ),
                # PUT /api/items/{id} - 更新
                APIEndpoint(
                    method="PUT",
                    path=f"{base_path}/{{id}}",
                    description=f"更新 {entity_name}",
                    request_schema=f"{entity_name}Update",
                    response_schema=entity_name,
                    tags=[entity_name]
                ),
                # DELETE /api/items/{id} - 删除
                APIEndpoint(
                    method="DELETE",
                    path=f"{base_path}/{{id}}",
                    description=f"删除 {entity_name}",
                    response_schema="SuccessResponse",
                    tags=[entity_name]
                ),
            ])

        # 根据 features 添加特殊端点
        for feature in features:
            if feature.type == "chart":
                endpoints.append(
                    APIEndpoint(
                        method="GET",
                        path="/api/statistics",
                        description="获取统计数据",
                        response_schema="StatisticsResponse",
                        tags=["Statistics"]
                    )
                )
            elif feature.type == "export":
                endpoints.append(
                    APIEndpoint(
                        method="GET",
                        path="/api/export",
                        description="导出数据",
                        response_schema="FileResponse",
                        tags=["Export"]
                    )
                )

        return endpoints

    def _generate_openapi(self, prd: PRD, endpoints: List[APIEndpoint]) -> Dict[str, Any]:
        """生成 OpenAPI 3.0 规范"""
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": f"{prd.app_name} API",
                "description": prd.description,
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": "http://localhost:8000",
                    "description": "开发服务器"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {}
            }
        }

        # 添加路径
        for endpoint in endpoints:
            path = endpoint.path
            if path not in openapi_spec["paths"]:
                openapi_spec["paths"][path] = {}

            method_lower = endpoint.method.lower()
            openapi_spec["paths"][path][method_lower] = {
                "summary": endpoint.description,
                "tags": endpoint.tags,
                "responses": {
                    "200": {
                        "description": "成功",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    }
                }
            }

        return openapi_spec

    def _plan_file_structure(self, prd: PRD) -> Dict[str, Any]:
        """规划文件结构"""
        file_tree = {
            "backend": {
                "app": {
                    "__init__.py": "Python 包初始化",
                    "main.py": "FastAPI 应用入口",
                    "database.py": "数据库配置",
                    "models.py": "SQLAlchemy 模型",
                    "routes.py": "API 路由"
                },
                "requirements.txt": "Python 依赖",
                "seed.py": "测试数据脚本"
            },
            "frontend": {
                "src": {
                    "main.jsx": "React 入口",
                    "App.jsx": "主应用组件",
                    "index.css": "全局样式",
                    "api": {
                        "client.js": "API 客户端"
                    },
                    "pages": {
                        f"{entity.name}List.jsx": f"{entity.name} 列表页"
                        for entity in prd.data_entities
                    }
                },
                "package.json": "Node 依赖",
                "vite.config.js": "Vite 配置",
                "tailwind.config.js": "Tailwind 配置",
                "index.html": "HTML 入口"
            },
            "README.md": "项目文档",
            "start.py": "启动脚本",
            "start_all.py": "统一启动器",
            ".gitignore": "Git 忽略文件"
        }

        return file_tree
