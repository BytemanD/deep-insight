from fastapi import APIRouter, Header

from deep_insight.apps.master.manager import MANAGER
from deep_insight.common.context import project_id

router = APIRouter(prefix="/docs")


@router.get("")
async def list_docs(x_project_id: str = Header(None)):
    token = project_id.set(x_project_id)
    try:
        docs = MANAGER.list_docs()
        return {"docs": docs}
    finally:
        project_id.reset(token)
