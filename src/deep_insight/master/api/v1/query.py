from fastapi import APIRouter, Header
from pydantic import BaseModel

from deep_insight.common.context import project_id
from deep_insight.master.manager import MANAGER

router = APIRouter(prefix="/query")


class QueryRequest(BaseModel):
    text: str


class QueryResponse(BaseModel):
    answer: str


@router.post("")
async def query(req: QueryRequest, x_project_id: str = Header(None)):
    token = project_id.set(x_project_id)
    try:
        answer = await MANAGER.llm_query(req.text, project_id=x_project_id)
        return QueryResponse(answer=answer)
    finally:
        project_id.reset(token)
