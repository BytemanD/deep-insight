from typing import List

from agents import function_tool

from deep_insight.common.context import project_id
from deep_insight.doc.store import DEFAULT_COLLECTION_NAME, SERVICE, Doc, RetrivalDoc


@function_tool(timeout=300)
async def list_docs() -> List[Doc]:
    """列出ChromaDB中的文档

    Returns:
        List[dict]: 所有匹配的文档列表
    """
    pid = project_id.get()
    collection = pid or DEFAULT_COLLECTION_NAME
    return [
        x.model_dump(mode="json") for x in SERVICE.list_docs(collection_name=collection)
    ]


@function_tool(timeout=300)
async def query(text: str, n_results: int = 1) -> List[RetrivalDoc]:
    """根据文本召回匹配的文档内容

    Args:
        text (str): 查询文本
        n_results (int, optional): 需要召回的文档数量. Defaults to 1.
    Returns:
        List[dict]: 所有匹配的文档内容列表
    """
    pid = project_id.get()
    collection = pid or DEFAULT_COLLECTION_NAME
    return [
        x.model_dump(mode="json")
        for x in SERVICE.query(text, n_results=n_results, collection_name=collection)
    ]
