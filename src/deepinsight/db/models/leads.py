"""Leads Model - 线索（核心输出表）"""

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from deepinsight.db.models.base import DBModel


class LeadPriority:
    """线索优先级枚举"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LeadStatus:
    """线索状态枚举"""

    NEW = "new"
    REVIEWING = "reviewing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class LeadStage:
    """线索阶段枚举"""

    EXPLORATION = "exploration"
    FEASIBILITY = "feasibility"
    TENDER = "tender"
    EPC = "epc"
    OPERATION = "operation"


class HypothesisStage:
    """假设阶段枚举"""

    SPARK = "spark"
    PROVISIONAL = "provisional"
    CORROBORATED = "corroborated"
    VALIDATED = "validated"
    PACKAGED = "packaged"


class Leads(DBModel):
    """线索"""

    __tablename__ = "leads"

    project_uuid: Mapped[str] = mapped_column(String(64), nullable=False, comment="项目ID")
    source: Mapped[str] = mapped_column(String(50), nullable=False, comment="线索来源")
    url: Mapped[str] = mapped_column(String(50), nullable=False, comment="线索url")
    match_reason: Mapped[str] = mapped_column(Text, nullable=True, comment="匹配理由")
    keywords: Mapped[str] = mapped_column(String, nullable=True, comment="关键词")

    title: Mapped[str] = mapped_column(String(500), nullable=False, comment="标题")
    summary: Mapped[str] = mapped_column(Text, nullable=True, comment="摘要")
    region: Mapped[str] = mapped_column(String(200), nullable=True, comment="地区")
    country: Mapped[str] = mapped_column(String(100), nullable=True, comment="国家")

    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="发布时间")

    type_uuid: Mapped[str] = mapped_column(String(50), nullable=False, comment="线索类型UUID")


class LeadTypes(DBModel):
    """线索类型"""

    __tablename__ = "lead_types"

    project_uuid: Mapped[str] = mapped_column(String(64), nullable=False, comment="项目ID")
    types: Mapped[str] = mapped_column(String(50), nullable=False, comment="线索类型")


class LeadSources(DBModel):
    """线索来源"""

    __tablename__ = "lead_sources"

    project_uuid: Mapped[str] = mapped_column(String(64), nullable=False, comment="项目ID")
    source: Mapped[str] = mapped_column(String(100), nullable=False, comment="线索来源")
