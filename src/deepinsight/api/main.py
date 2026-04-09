from fastapi import FastAPI, Request
from loguru import logger

from deepinsight.api.middleware.logging import logging_middleware
from deepinsight.api.v1 import leads
from deepinsight.db.utils import create_all_tables


async def lifespan(app: FastAPI):
    # 启动时
    logger.info("创建...")

    create_all_tables()
    yield
    # 关闭时
    logger.info("关闭中...")


app = FastAPI(title="DeepInsight API", lifespan=lifespan)

# 自定义中间件
app.middleware("http")(logging_middleware)
# app.middleware("http")(rate_limit.rate_limit_middleware)


# 注册路由


@app.get("/health")
def health(request: Request) -> dict:
    return {"status": "ok"}


app.include_router(leads.router, prefix="/api/v1", tags=["leads"])
