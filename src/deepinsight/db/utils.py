from pathlib import Path

from loguru import logger

from deepinsight.common.config import CONF
from deepinsight.db.models.base import DBModel, sync_engine


def create_all_tables():
    """创建所有表"""
    if CONF.db.url.startswith("sqlite:"):
        logger.warning("SQLite is not recommended for production use.")
        Path(CONF.db.url.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    logger.info("Creating all tables...")
    DBModel.metadata.create_all(bind=sync_engine)
    logger.success("All tables created successfully.")
