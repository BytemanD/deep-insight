from deep_insight.doc.store import SERVICE
from deep_insight.research.ai import ResearchAI


class MasterManager:
    def __init__(self):
        self.llm = ResearchAI()

    def list_docs(self):
        return SERVICE.list_docs()

    async def llm_query(self, text: str):
        await self.llm.query(text)

    def retrival(self, text: str):
        return SERVICE.query(text)


MANAGER = MasterManager()
