from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from deep_insight.apps.vector.manager import get_vector_driver
from deep_insight.db.models import Project, Session
from deep_insight.research.ai import ResearchAI


class Message(BaseModel):
    role: str = "user"
    content: str = ""
    thinking: str = ""


class MasterManager:
    def __init__(self):
        self.vector_driver = get_vector_driver()
        self.llm = ResearchAI()

    def list_docs(self):
        return self.vector_driver.list_docs()

    def create_project(self, name: str, description: Optional[str]):
        item = Project(name=name, description=description)
        item.create()
        return item

    def list_project(self):
        return Project.query()

    def delete_project(self, uuid: str):
        db_model = Project.get_by_uuid(uuid)
        if not db_model:
            raise Exception(f"Project {uuid} not found")
        db_model.delete()

    def list_session(self):
        """Project manager"""
        return Session.query()

    def create_session(self, name: str, project: Optional[str]):
        db_project = Project.get_by_uuid(project)
        if not db_project:
            raise Exception(f"Project {project} not found")
        item = Session(project_uuid=project, name=name)
        item.create()
        return item

    def delete_session(self, uuid: str):
        db_dialog = Session.get_by_uuid(uuid)
        if not db_dialog:
            raise Exception(f"Session {uuid} not found")

        db_dialog.delete()

    def retrival(self, text: str):
        return self.vector_driver.query(text)

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
            yield f"data: {chunk}\n\n"


MANAGER = MasterManager()
