import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, create_engine, event
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker

from deepinsight.common.config import CONF
from deepinsight.common.exceptions import AlreadyExistsError, DoesNotExistError, NotFoundError

Base = declarative_base()

sync_engine = create_engine(
    CONF.db.url,
    pool_size=CONF.db.pool_size,
    max_overflow=CONF.db.max_overflow,
    pool_timeout=CONF.db.pool_timeout,
    pool_recycle=CONF.db.pool_recycle,
    echo=CONF.db.echo,
)

# Sync session factory
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)


class DBModel(Base):
    """所有模型的基类，包含通用的 id、uuid、create_at、update_at 字段"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 非 DB 属性：存储加载时的原始值
    _changes: dict = {}

    def __setattr__(self, name, value):
        """支持 dict-like 访问"""
        if name not in self.__table__.columns.keys():
            object.__setattr__(self, name, value)
        if getattr(self, name) != value:
            self._changes[name] = value
        object.__setattr__(self, name, value)

    def _get_changes(self) -> dict:
        """返回字段名到 (原值, 新值) 的映射"""
        return {
            k: v
            for k, v in self._changes.items()
            if k not in ["id", "uuid", "created_at", "updated_at"] and hasattr(self, k)
        }

    @classmethod
    def query(cls, *criterion, **filters):
        """返回一个 QueryBuilder 用于链式查询"""
        with SyncSessionLocal() as session:
            query = session.query(cls)
            if criterion:
                query = query.filter(*criterion)
            elif filters:
                query = query.filter_by(**filters)
        return query

    @classmethod
    def get_by_id(cls, id: str):
        with SyncSessionLocal() as session:
            result = session.query(cls).filter(cls.id == id).first()
            if result is None:
                raise NotFoundError(cls, id=id)
            return result

    @classmethod
    def get_by_uuid(cls, uuid: str):
        with SyncSessionLocal() as session:
            result = session.query(cls).filter(cls.uuid == uuid).first()
            if result is None:
                raise NotFoundError(cls, uuid=uuid)
            return result

    @classmethod
    def delete_by_uuid(cls, uuid: str) -> None:
        """根据 id 删除记录"""
        with SyncSessionLocal() as session:
            model = session.query(cls).filter(cls.uuid == uuid).first()
            if model is None:
                raise NotFoundError(cls, id=id)
            session.delete(model)
            session.commit()

    @classmethod
    def update_by_uuid(cls, uuid: str, **kwargs) -> None:
        """根据 id 删除记录"""
        with SyncSessionLocal() as session:
            session.query(cls).filter(cls.uuid == uuid).update(kwargs)
            session.commit()

    def _get_updated(self) -> dict:
        updated = {}
        for field in self.__table__.columns.keys():
            if field in ["id", "uuid", "create_at", "update_at"]:
                continue

            updated[field] = getattr(self, field)

    def save(self):
        """更新当前实例到数据库，id 不存在则抛出异常"""
        if self.id is None:
            raise DoesNotExistError(self.__class__)
        changes = self._get_changes()
        if not changes:
            return
        with SyncSessionLocal() as session:
            session.query(self.__class__).filter_by(id=self.id).update(changes)
            session.commit()

    def create(self):
        """创建新记录到数据库，id 已存在则抛出异常"""
        if self.id is not None or self.uuid is not None:
            raise AlreadyExistsError(self.__class__, id=self.id, uuid=self.uuid)
        # self.uuid = generate_uuid()
        with SyncSessionLocal() as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self):
        """删除当前实例"""
        with SyncSessionLocal() as session:
            session.delete(self)
            session.commit()


@event.listens_for(DBModel, "before_insert", propagate=True)
def set_uuid_create_at(mapper, connection, target: DBModel):
    """插入时自动设置 uuid、create_at 和 update_at"""
    if target.uuid is None:
        target.uuid = str(uuid.uuid4())
    if target.created_at is None:
        target.created_at = datetime.now()
    if target.updated_at is None:
        target.updated_at = datetime.now()


@event.listens_for(DBModel, "before_update", propagate=True)
def set_update_at(mapper, connection, target):
    """更新时自动设置 update_at"""
    target.updated_at = datetime.now()
