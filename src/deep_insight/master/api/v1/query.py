from fastapi import APIRouter
from pydantic import BaseModel

from deep_insight.master.manager import MANAGER

router = APIRouter(prefix="/query")


class QueryRequest(BaseModel):
    text: str


class QueryResponse(BaseModel):
    answer: str


@router.post("")
async def query(req: QueryRequest):
    answer = await MANAGER.llm_query(req.text)
    return QueryResponse(answer=answer)
