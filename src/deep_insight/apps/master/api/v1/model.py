from fastapi import APIRouter

from deep_insight.apps.master.manager import MANAGER

router = APIRouter(prefix="/models")


@router.get("")
async def query():
    return {"models": MANAGER.get_models()}
