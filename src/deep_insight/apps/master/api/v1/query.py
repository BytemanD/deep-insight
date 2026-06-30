from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from deep_insight.apps.master.manager import MANAGER
from deep_insight.common.context import project_id

router = APIRouter(prefix="/agents")


class QueryRequest(BaseModel):
    text: str


@router.post("/{session_id}/chat")
async def query(
    session_id: str,
    req: QueryRequest,
    x_project_id: str = Header(None),
):
    async def event_stream():
        token = project_id.set(x_project_id)
        try:
            async for chunk in MANAGER.streaming_llm_query(
                req.text, session_id=session_id
            ):
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
