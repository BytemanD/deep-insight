from fastapi import APIRouter

from deep_insight.master.manager import MANAGER

router = APIRouter(prefix="/docs")


@router.get("")
async def list_docs():
    docs = MANAGER.list_docs()
    return {"docs": docs}
