from fastapi import HTTPException
from pydantic import BaseModel

from deep_insight.db.models import Session
from deep_insight.doc.store import DocStore
from deep_insight.research.ai import ResearchAI


class Message(BaseModel):
    role: str = "user"
    content: str = ""
    thinking: str = ""


class MasterManager:
    def __init__(self):
        self.doc_store = DocStore()
        self.llm = ResearchAI()

    def list_docs(self):
        return self.doc_store.list_docs()

    def retrival(self, text: str):
        return self.doc_store.query(text)

    async def delete_session(self, session_id: str):
        session = Session.get_by_uuid(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        session.delete()
        await self.llm.clear_session_items(session_id)

    async def llm_query(self, text: str, project_id: str = None):
        return await self.llm.query(text)

    async def list_messages(self, session_id: str = None):
        session = Session.get_by_uuid(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        items = await self.llm.list_messages(session_id=session.uuid)
        messages = []
        for x in items:
            if x.get("role") == "user":
                messages.append(Message(role="user", content=x.get("content")))
            elif x.get("role") == "assistant":
                content = x.get("content") or []
                for content in x.get("content") or []:
                    messages.append(
                        Message(
                            role="assistant",
                            content=content.get("text")
                            if content and content.get("type") == "output_text"
                            else "",
                        )
                    )
        return messages

    async def streaming_llm_query(self, text: str, session_id: str = None):
        async for chunk in self.llm.streaming_query(text, session_id=session_id):
            yield chunk


MANAGER = MasterManager()
