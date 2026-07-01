from datetime import datetime
from typing import Optional
from uuid import uuid4

from loguru import logger
from sqlmodel import Field, SQLModel, delete, select

from deep_insight.db import database


class BaseSQLModel(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(nullable=False, index=True, unique=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def query(cls, *criterion, **filters):
        stm = select(cls)
        if criterion:
            stm = stm.filter(*criterion)
        elif filters:
            stm = stm.filter_by(**filters)

        return database.exec(stm)

    @classmethod
    def get_by_uuid(cls, uuid: str) -> Optional["BaseSQLModel"]:
        stm = select(cls).where(cls.uuid == uuid)
        return database.query_first(stm)

    def update(self):
        database.update(self)

    def delete(self):
        """创建新记录到数据库, id 已存在则抛出异常"""
        stm = delete(self.__class__).where(self.__class__.uuid == self.uuid)
        database.exec(stm)

    def create(self):
        """创建新记录到数据库, id 已存在则抛出异常"""
        if self.id is not None or self.uuid is not None:
            raise ValueError(f"{self.__class__} is already created")

        if self.uuid is None:
            self.uuid = str(uuid4())
        database.add(self)


class Project(BaseSQLModel, table=True):
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)


class Session(BaseSQLModel, table=True):
    project_uuid: str = Field(nullable=False, index=True)
    name: str = Field(nullable=True)


class Doc(BaseSQLModel, table=True):
    project_uuid: str = Field(nullable=False, index=True)
    name: str = Field(nullable=False)
    file_size: int = Field(nullable=False)
    file_path: str = Field(nullable=False)
    status: str = Field(nullable=False, default="pending")


def create_all_tables():
    logger.debug("create all tables")
    SQLModel.metadata.create_all(database.engine)
