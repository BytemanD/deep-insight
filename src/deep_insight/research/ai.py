import json
import textwrap
from pathlib import Path
from typing import Optional
from uuid import uuid4

import dotenv
from agents import Agent, Runner, SQLiteSession, stream_events
from loguru import logger
from openai.types.responses import (
    ResponseCreatedEvent,
    ResponseFailedEvent,
    ResponseInProgressEvent,
)
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from deep_insight.common.utils import text_shorten
from deep_insight.research import tools

dotenv.load_dotenv()

# instructions = """
# 你是一个文档分析专家, 你的任务是根据用户的问题, 从ChromaDB知识库中检索出最相关的文档，并给出答案。
# 你的回答必须遵循以下规则：
# 1. 必须基于检索到的文档
# 2. 如果找不到相关的文档，请返回 "没有找到相关的文档"
# 3. 你的回答必须标注是根据哪个文档得出的结论

# 你的回答。
# """

instructions = """
你是一个文档分析专家。
"""


class ResearchAI:
    def __init__(self):
        self.session_store_path = Path("data", "conversation.db")
        # atexit.register(self.agent.)
        # set_default_openai_client(self.openai, use_for_tracing=False)
        # if conf.CONF.agent.openai_api:
        #     set_default_openai_api(conf.CONF.agent.openai_api)
        # set_tracing_disabled(True)
        self.console = Console()

        self.agent = Agent(
            name="AI-Shell",
            instructions=instructions,
            model="qwen3.7-max-2026-05-20",
            tools=[
                tools.list_docs,
                tools.query,
            ],
        )

    def _get_session(self, session_id: Optional[str] = None):
        return SQLiteSession(
            session_id or str(uuid4()),
            db_path=self.session_store_path,
        )

    async def query(
        self,
        text: str,
        session_id: Optional[str] = None,
    ):
        logger.debug("输入: {}", text)

        result = Runner.run_streamed(
            self.agent,
            text,
            session=self._get_session(session_id=session_id),
            max_turns=102400,
            # NOTE: 使用了本地本地会话持久化后不能使用以下参数
            # auto_previous_response_id=True,
            # previous_response_id=self.response_id,
        )
        llm_answer = ""
        async for event in result.stream_events():
            if isinstance(event, stream_events.AgentUpdatedStreamEvent):
                self.console.print(
                    f"[切换Agent]: {event.new_agent.name}", style="grey0"
                )
                continue
                # 通知用户 Agent 正在切换
            elif isinstance(event, stream_events.RawResponsesStreamEvent):
                if hasattr(event.data, "delta"):
                    # print(event.data.delta, flush=True, end='')
                    pass
                elif isinstance(
                    event.data, (ResponseInProgressEvent, ResponseCreatedEvent)
                ):
                    self.console.print(
                        f"[状态] {event.data.response.status}", style="grey0"
                    )
                elif isinstance(event.data, ResponseFailedEvent):
                    logger.debug(
                        "received response failed event: {}", event.data.response.error
                    )
                    logger.error("收到错误事件: {}", event.data.response.error)
                    # if conf.CONF.ai_shell.show_failed_event:
                    #     self.console.print(
                    #         Panel(
                    #             event.data.response.error.model_dump_json(),
                    #             title="收到错误事件",
                    #             border_style="red",
                    #         ),
                    #     )
                else:
                    pass
                continue
            elif event.name == "tool_called":
                # 向用户展示工具调用状态
                self.console.print(
                    f"[选择工具] {event.item.raw_item.name}, 参数： {event.item.raw_item.arguments}",
                    style="grey0",
                )
                logger.info(
                    "选择工具: {}, 参数: {}",
                    event.item.raw_item.name,
                    event.item.raw_item.arguments,
                )
                continue
            elif event.name == "tool_output":
                logger.info("工具输出: {}", text_shorten(event.item.output))
                continue
            elif isinstance(event, stream_events.RunItemStreamEvent):
                logger.debug("RunItemStreamEvent raw_item: {}", event.item.raw_item)
                if event.item.raw_item.content:
                    for content in event.item.raw_item.content:
                        if not content.text:
                            continue
                        llm_answer += content.text
                        self.console.print(
                            Panel(
                                Markdown(content.text), title="AI", border_style="cyan"
                            )
                        )
                elif event.item.raw_item.summary:
                    for sumary in event.item.raw_item.summary:
                        self.console.print(
                            textwrap.indent(sumary.text.rstrip(), "> "), style="grey0"
                        )
                continue
            else:
                logger.debug("other event: {}", event)
        return llm_answer

    async def streaming_query(
        self,
        text: str,
        session_id: Optional[str] = None,
    ):
        logger.debug("query({}): {}", session_id, text)

        result = Runner.run_streamed(
            self.agent,
            text,
            session=self._get_session(session_id),
            max_turns=102400,
        )
        async for event in result.stream_events():
            if isinstance(event, stream_events.AgentUpdatedStreamEvent):
                yield json.dumps(
                    {"type": "info", "content": f"切换Agent: {event.new_agent.name}"}
                )
                continue
            elif isinstance(event, stream_events.RawResponsesStreamEvent):
                if hasattr(event.data, "delta") and event.data.delta:
                    yield json.dumps({"type": "thinking", "content": event.data.delta})
                elif isinstance(event.data, ResponseFailedEvent):
                    logger.warning(
                        "received response failed event: {}", event.data.response.error
                    )
                    logger.error("收到错误事件: {}", event.data.response.error)
                    yield json.dumps(
                        {"type": "error", "content": str(event.data.response.error)}
                    )
                continue
            elif event.name == "tool_called":
                logger.info(
                    "选择工具: {}, 参数: {}",
                    event.item.raw_item.name,
                    event.item.raw_item.arguments,
                )
                yield json.dumps(
                    {"type": "info", "content": f"使用工具: {event.item.raw_item.name}"}
                )
                continue
            elif event.name == "tool_output":
                logger.info("工具输出: {}", text_shorten(event.item.output))
                continue
            elif isinstance(event, stream_events.RunItemStreamEvent):
                if event.item.raw_item.content:
                    for content in event.item.raw_item.content:
                        if not content.text:
                            continue
                        yield json.dumps({"type": "text", "content": content.text})
                continue
        yield "[DONE]"

    async def list_messages(self, session_id: Optional[str] = None):
        logger.debug("list messages of session {}", session_id)
        session = self._get_session(session_id=session_id)
        return await session.get_items()

    async def clear_session_items(self, session_id: str):
        logger.debug("clear session {}", session_id)
        session = self._get_session(session_id=session_id)
        await session.clear_session()
