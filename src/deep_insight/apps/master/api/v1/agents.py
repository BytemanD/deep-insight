from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from deep_insight.apps.master.manager import MANAGER

router = APIRouter(prefix="/agents")


class QueryRequest(BaseModel):
    text: str
    model: str = ""


@router.post("/{session_id}/chat")
async def query(
    session_id: str,
    req: QueryRequest,
):
    async def event_stream():
        async for chunk in MANAGER.streaming_llm_query(
            req.text, session_id=session_id, model=req.model
        ):
            yield chunk

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
