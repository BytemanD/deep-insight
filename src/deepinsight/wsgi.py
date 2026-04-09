import uvicorn
from fastapi import FastAPI
from loguru import logger

from augur_common import logging
from augur_common.config import CONF


def launch(app: FastAPI, debug_app: str, host: str = "localhost", port: int = 8000):
    logging.setup_logging()
    if CONF.debug:
        # 开发模式：启用自动重载
        logger.warning("启动开发模式")
        uvicorn.run(debug_app, host=host, port=port, reload=True)
    else:
        # 生产模式
        uvicorn.run(app, host="0.0.0.0", port=port)
