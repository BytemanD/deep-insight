from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from deep_insight.apps.master.api.v1 import agents, doc, model, project, session
from deep_insight.apps.master.middleware import ProjectContextMiddleware
from deep_insight.db.models import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("start Master ...")
    create_all_tables()
    yield
    logger.info("stop Master ...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(ProjectContextMiddleware)

app.include_router(doc.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(project.router, prefix="/api/v1")
app.include_router(session.router, prefix="/api/v1")
app.include_router(model.router, prefix="/api/v1")
