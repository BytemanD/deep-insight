"""数据库初始化工具 - 创建表并添加 mock 数据"""

import argparse
import uuid

from augur_common.database import SyncSessionLocal, sync_engine
from loguru import logger
from sqlalchemy import text

from augur_common.config import CONF
from augur_common.db.init_db import create_all_tables
from augur_common.db.models.base import BaseModel


def init_database():
    """初始化数据库连接"""
    logger.info(f"Database URL: {CONF.database.url}")
    logger.info("Database initialized successfully.")


def drop_all_tables():
    """删除所有表"""
    logger.info("Dropping all tables...")
    BaseModel.metadata.drop_all(bind=sync_engine)
    logger.info("All tables dropped successfully.")


def generate_uuid() -> str:
    """生成短 UUID"""
    return uuid.uuid4().hex[:16]


def reset_database():
    """重置数据库（删除所有表并重新创建）"""
    drop_all_tables()
    create_all_tables()


def show_tables():
    """显示所有表"""
    session = SyncSessionLocal()
    try:
        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        tables = result.fetchall()
        logger.info("Tables in database:")
        for table in tables:
            logger.info(f"  - {table[0]}")
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="AUGUR 数据库初始化工具")
    parser.add_argument("action", choices=["init", "create", "drop", "reset", "mock", "tables"], help="操作类型")
    args = parser.parse_args()

    if args.action == "init":
        init_database()
    elif args.action == "create":
        create_all_tables()
    elif args.action == "drop":
        drop_all_tables()
    elif args.action == "reset":
        reset_database()
    elif args.action == "tables":
        show_tables()


if __name__ == "__main__":
    main()
