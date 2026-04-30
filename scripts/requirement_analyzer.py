"""
需求分析器 - 阶段1：需求澄清

将用户的模糊描述转化为结构化的产品需求文档（PRD）
"""

import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field as PydanticField

try:
    from .utils import setup_logger, to_snake_case, to_pascal_case
    from .config_manager import ConfigManager
except ImportError:
    from utils import setup_logger, to_snake_case, to_pascal_case
    from config_manager import ConfigManager


logger = setup_logger(__name__)


# ===== Pydantic 数据模型 =====

class FieldDef(BaseModel):
    """字段定义"""
    type: str = PydanticField(description="字段类型：string, integer, float, boolean, datetime, text")
    required: bool = PydanticField(default=True, description="是否必填")
    description: str = PydanticField(default="", description="字段描述")
    default: Optional[str] = PydanticField(default=None, description="默认值")


class Entity(BaseModel):
    """数据实体"""
    name: str = PydanticField(description="实体名称（PascalCase）")
    description: str = PydanticField(default="", description="实体描述")
    fields: Dict[str, FieldDef] = PydanticField(default_factory=dict, description="字段定义")
    relationships: List[str] = PydanticField(default_factory=list, description="关系描述")


class Feature(BaseModel):
    """功能需求"""
    id: str = PydanticField(description="功能ID")
    name: str = PydanticField(description="功能名称")
    type: str = PydanticField(default="form", description="功能类型：form, list, detail, chart, export")
    priority: str = PydanticField(default="medium", description="优先级：high, medium, low")
    description: str = PydanticField(default="", description="功能描述")
    ui_elements: List[str] = PydanticField(default_factory=list, description="UI元素")
    data_flow: str = PydanticField(default="", description="数据流描述")


class PRD(BaseModel):
    """产品需求文档"""
    app_name: str = PydanticField(description="应用名称")
    description: str = PydanticField(default="", description="应用描述")
    tech_stack: str = PydanticField(default="react-fastapi", description="技术栈")
    features: List[Feature] = PydanticField(default_factory=list, description="功能列表")
    data_entities: List[Entity] = PydanticField(default_factory=list, description="数据实体列表")
    user_roles: List[str] = PydanticField(default_factory=lambda: ["user"], description="用户角色")
    auth_required: bool = PydanticField(default=False, description="是否需要认证")
    warnings: List[str] = PydanticField(default_factory=list, description="警告信息")


# Keep backward-compatible alias
Field = FieldDef


# ===== 需求分析器 =====

class RequirementAnalyzer:
    """需求分析器"""

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        初始化需求分析器

        Args:
            config_manager: 配置管理器（可选）
        """
        self.config = config_manager or ConfigManager()
        self.max_features = self.config.get_max_features()

        # 实体关键词（用于识别数据实体）
        self.entity_keywords = {
            '用户': 'User',
            '商品': 'Product',
            '订单': 'Order',
            '任务': 'Task',
            '项目': 'Project',
            '支出': 'Expense',
            '收入': 'Income',
            '分类': 'Category',
            '标签': 'Tag',
            '评论': 'Comment',
            '文章': 'Article',
            '书籍': 'Book',
        }

        # 操作关键词（用于识别功能需求）
        self.operation_keywords = {
            '添加': 'create',
            '创建': 'create',
            '新建': 'create',
            '查看': 'read',
            '浏览': 'read',
            '列表': 'list',
            '编辑': 'update',
            '修改': 'update',
            '更新': 'update',
            '删除': 'delete',
            '统计': 'chart',
            '图表': 'chart',
            '导出': 'export',
            '搜索': 'search',
            '筛选': 'filter',
        }

    def analyze(self, user_input: str) -> PRD:
        """
        分析用户输入，生成 PRD

        Args:
            user_input: 用户的需求描述

        Returns:
            PRD 对象
        """
        logger.info("开始需求分析")

        # 提取应用名称
        app_name = self._extract_app_name(user_input)

        # 提取数据实体
        entities = self._extract_entities(user_input)

        # 提取功能需求
        features = self._extract_features(user_input, entities)

        # 生成应用描述
        description = self._generate_description(user_input, entities, features)

        # 检查功能数量
        warnings = []
        if len(features) > self.max_features:
            warnings.append(
                f"检测到 {len(features)} 个功能请求，超出推荐限制（≤ {self.max_features} 个核心功能）。"
                "建议优先实现核心功能，其余功能可延后迭代。"
            )

        prd = PRD(
            app_name=app_name,
            description=description,
            tech_stack="react-fastapi",
            features=features,
            data_entities=entities,
            warnings=warnings
        )

        logger.info(f"需求分析完成：{len(entities)} 个实体，{len(features)} 个功能")
        return prd

    def _extract_app_name(self, text: str) -> str:
        """提取应用名称"""
        # 简单的规则：查找"XXX软件"、"XXX系统"、"XXX应用"等模式
        patterns = [
            r'做一个(.+?)[软件系统应用工具]',
            r'创建一个(.+?)[软件系统应用工具]',
            r'生成一个(.+?)[软件系统应用工具]',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                return to_pascal_case(to_snake_case(name))

        # 默认名称
        return "MyApp"

    def _extract_entities(self, text: str) -> List[Entity]:
        """提取数据实体"""
        entities = []

        # 使用关键词匹配
        for keyword, entity_name in self.entity_keywords.items():
            if keyword in text:
                entity = self._create_entity(entity_name, text)
                if entity:
                    entities.append(entity)

        # 如果没有识别到实体，创建一个默认实体
        if not entities:
            entities.append(self._create_default_entity())

        return entities

    def _create_entity(self, entity_name: str, context: str) -> Optional[Entity]:
        """创建实体"""
        # 根据实体类型定义通用字段
        common_fields = {
            "name": Field(
                type="string",
                required=True,
                description="名称"
            ),
            "description": Field(
                type="text",
                required=False,
                description="描述"
            ),
        }

        # 根据实体类型添加特定字段
        specific_fields = {}

        if entity_name == "Expense":
            specific_fields = {
                "amount": Field(type="float", required=True, description="金额"),
                "category": Field(type="string", required=True, description="分类"),
                "date": Field(type="datetime", required=True, description="日期"),
            }
        elif entity_name == "Task":
            specific_fields = {
                "title": Field(type="string", required=True, description="标题"),
                "priority": Field(type="string", required=False, description="优先级"),
                "status": Field(type="string", required=True, description="状态"),
                "due_date": Field(type="datetime", required=False, description="截止日期"),
            }
        elif entity_name == "Product":
            specific_fields = {
                "price": Field(type="float", required=True, description="价格"),
                "stock": Field(type="integer", required=False, description="库存"),
            }
        elif entity_name == "Order":
            specific_fields = {
                "total_amount": Field(type="float", required=True, description="总金额"),
                "status": Field(type="string", required=True, description="订单状态"),
            }

        # 合并字段（只保留特定字段，去掉通用字段以避免重复）
        if specific_fields:
            fields = specific_fields
        else:
            fields = common_fields

        return Entity(
            name=entity_name,
            description=f"{entity_name} 实体",
            fields=fields
        )

    def _create_default_entity(self) -> Entity:
        """创建默认实体"""
        return Entity(
            name="Item",
            description="默认数据项",
            fields={
                "name": Field(type="string", required=True, description="名称"),
                "description": Field(type="text", required=False, description="描述"),
            }
        )

    def _extract_features(self, text: str, entities: List[Entity]) -> List[Feature]:
        """提取功能需求"""
        features = []

        # 基于实体生成 CRUD 功能
        for entity in entities:
            entity_lower = entity.name.lower()

            # 创建功能
            if any(kw in text for kw in ['添加', '创建', '新建', '记录']):
                features.append(Feature(
                    id=f"create_{entity_lower}",
                    name=f"创建{entity.name}",
                    type="form",
                    priority="high",
                    description=f"添加新的{entity.name}记录",
                    ui_elements=["表单", "输入框", "提交按钮"],
                    data_flow="用户输入 → API POST → 数据库"
                ))

            # 列表功能
            if any(kw in text for kw in ['查看', '浏览', '列表', '展示']):
                features.append(Feature(
                    id=f"list_{entity_lower}",
                    name=f"{entity.name}列表",
                    type="list",
                    priority="high",
                    description=f"查看所有{entity.name}记录",
                    ui_elements=["表格/卡片", "翻页", "搜索框"],
                    data_flow="API GET → 数据库 → 列表展示"
                ))

            # 编辑功能
            if any(kw in text for kw in ['编辑', '修改', '更新']):
                features.append(Feature(
                    id=f"update_{entity_lower}",
                    name=f"编辑{entity.name}",
                    type="form",
                    priority="medium",
                    description=f"修改{entity.name}记录",
                    ui_elements=["表单", "输入框", "更新按钮"],
                    data_flow="加载数据 → 用户修改 → API PUT → 数据库"
                ))

            # 删除功能
            if any(kw in text for kw in ['删除']):
                features.append(Feature(
                    id=f"delete_{entity_lower}",
                    name=f"删除{entity.name}",
                    type="detail",
                    priority="low",
                    description=f"删除{entity.name}记录",
                    ui_elements=["删除按钮", "确认对话框"],
                    data_flow="用户确认 → API DELETE → 数据库"
                ))

        # 统计图表功能
        if any(kw in text for kw in ['统计', '图表', '分析']):
            features.append(Feature(
                id="statistics",
                name="数据统计",
                type="chart",
                priority="medium",
                description="数据统计和可视化",
                ui_elements=["图表", "筛选器"],
                data_flow="API GET → 统计计算 → 图表展示"
            ))

        # 导出功能
        if any(kw in text for kw in ['导出', 'Excel', 'CSV']):
            features.append(Feature(
                id="export",
                name="数据导出",
                type="export",
                priority="low",
                description="导出数据为 Excel 或 CSV",
                ui_elements=["导出按钮", "格式选择"],
                data_flow="用户选择 → API GET → 文件生成 → 下载"
            ))

        return features

    def _generate_description(
        self,
        user_input: str,
        entities: List[Entity],
        features: List[Feature]
    ) -> str:
        """生成应用描述"""
        entity_names = "、".join([e.name for e in entities])
        return f"一个用于管理 {entity_names} 的 Web 应用，支持 {len(features)} 个核心功能。"
