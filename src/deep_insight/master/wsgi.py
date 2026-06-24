from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from deep_insight.db.models import create_all_tables
from deep_insight.master.api.v1 import doc, query


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动前执行
    logger.info("start Master ...")
    create_all_tables()
    yield  # 应用运行期间
    logger.info("stop Master ...")


app = FastAPI(lifespan=lifespan)

app.include_router(doc.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
