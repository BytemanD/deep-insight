"""Leads Model - 线索（核心输出表）"""

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from deepinsight.db.models.base import DBModel


class Project(DBModel):
    __tablename__ = "leads"

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="项目名")
    prompt: Mapped[str] = mapped_column(Text, nullable=True, comment="提示词")
    rule: Mapped[list[str]] = mapped_column(JSON(200), nullable=True, comment="匹配规则")
