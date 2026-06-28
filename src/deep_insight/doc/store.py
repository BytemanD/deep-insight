from pathlib import Path
from typing import List, Optional

import chromadb
import click
from loguru import logger
from pydantic import BaseModel

from deep_insight.common import context
from deep_insight.common.utils import file_sha256


class Doc(BaseModel):
    file_path: str


class RetrivalDoc(BaseModel):
    id: str
    name: str
    distance: Optional[float] = 0
    content: Optional[str] = ""
    metadata: Optional[dict] = {}


DEFAULT_COLLECTION_NAME = "deep_insight"


class DocStore:
    def __init__(self, path: str = "data/chromadb"):
        db_path = Path(path)
        if not db_path.exists():
            db_path.mkdir(parents=True)
        self.client = chromadb.PersistentClient(path=db_path)

    def _get_collection(self, collection_name: Optional[str] = None):
        return self.client.get_or_create_collection(
            name=collection_name or context.project_id.get() or DEFAULT_COLLECTION_NAME
        )

    def import_file(
        self,
        file_path: str,
    ):
        collection = self._get_collection()
        logger.debug("read file: {} ...", file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        doc_id = file_sha256(file_path)
        logger.debug("document id: {}", doc_id)
        docs = collection.get(doc_id)
        if docs.get("ids"):
            raise click.ClickException("document already exists")

        logger.debug("add document to project {} ...", collection.name)
        collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[{"file_name": Path(file_path).name}],
        )

    def list_docs(self):
        logger.info("")
        collection = self._get_collection()
        logger.info("list docs, collection_name={}", collection.name)
        try:
            result = collection.get(include=["metadatas"])
        except Exception as e:
            logger.exception("list docs error, collection_name={}", collection.name)
            raise e

        logger.debug("result: {}", result)
        docs = [
            RetrivalDoc(
                id=doc_id,
                name=(result["metadatas"][index] or {}).pop("file_name", ""),
                metadata=result["metadatas"][index] or {},
            )
            for index, doc_id in enumerate(result["ids"])
            if result["metadatas"] and result["metadatas"][index]
        ]
        logger.success("return {} docs", len(docs))
        return docs

    def query(
        self,
        text: str,
        n_results=1,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> List[RetrivalDoc]:
        collection = self._get_collection(collection_name)
        results = collection.query(query_texts=[text], n_results=n_results)
        logger.info(
            "query, collection_name={}, n_results={}", collection_name, n_results
        )
        if not results["ids"]:
            logger.warning("no docs found")
            return []
        docs = [
            RetrivalDoc(
                name=(results["metadatas"][0][index] or {}).get("file_name"),
                metadata=results["metadatas"][0][index] or {},
                distance=results["distances"][0][index] or 0,
                content=results["documents"][0][index] or "",
            )
            for index, _ in enumerate(results["ids"][0])
        ]
        logger.success("return {} docs", len(docs))
        return docs


SERVICE = DocStore()
