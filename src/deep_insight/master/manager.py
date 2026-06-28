from deep_insight.doc.store import SERVICE
from deep_insight.research.ai import ResearchAI


class MasterManager:
    def __init__(self):
        self.llm = ResearchAI()

    def list_docs(self):
        return SERVICE.list_docs()

    async def llm_query(self, text: str, project_id: str = None):
        return await self.llm.query(text)

    async def list_messages(self):
        return await self.llm.query()

    async def streaming_llm_query(self, text: str, session_id: str = None):
        async for chunk in self.llm.streaming_query(text, session_id=session_id):
            yield chunk

    def retrival(self, text: str):
        return SERVICE.query(text)


MANAGER = MasterManager()
