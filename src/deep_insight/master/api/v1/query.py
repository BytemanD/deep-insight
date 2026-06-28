from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from deep_insight.common.context import project_id
from deep_insight.master.manager import MANAGER

router = APIRouter(prefix="/query")


class QueryRequest(BaseModel):
    text: str


@router.post("")
async def query(
    req: QueryRequest,
    x_project_id: str = Header(None),
    x_session_id: str = Header(None),
):
    async def event_stream():
        token = project_id.set(x_project_id)
        try:
            async for chunk in MANAGER.streaming_llm_query(
                req.text, session_id=x_session_id
            ):
                print("=======> ", chunk)
                yield chunk
        finally:
            project_id.reset(token)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
