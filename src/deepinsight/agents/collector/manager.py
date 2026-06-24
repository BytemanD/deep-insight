from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from loguru import logger

from deepinsight.common.config import CONF


@tool
def collect_leads() -> str:
    """全球储能线索收集技能

    Returns the skill's prompt and context.
    """
    skill_path = Path("skills", "energy-storage-collector", "SKILL.md")
    return skill_path.read_text(encoding="utf-8")



tools = []

class CollectorManager:
    def __init__(self):
        # 创建模型实例
        self.llm = ChatOpenAI(
            base_url=CONF.collector.openai_base_url,
            api_key=CONF.collector.openai_api_key,  # API密钥
            model=CONF.collector.model,
            temperature=0.7,  # 随机性（0-1，越高越随机）
            max_tokens=500,  # 最大输出长度
            timeout=60,  # 请求超时（秒）
            max_retries=2,  # 失败重试次数
        )
        # print(self.collect_leads())
        self.agent = create_agent(
            self.llm, system_prompt="你是一个专业的情报收集助手", tools=[collect_leads] + tools
        )

    def run(self):
        # 创建浏览器实例
        from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
        from langchain_community.tools.playwright.utils import create_async_playwright_browser
        async_browser = create_async_playwright_browser()
        toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
        tools = toolkit.get_tools()

        # prompt = ChatPromptTemplate.from_messages([

        #     {"role": "system", "content": "你是一个浏览器自动化助手，可以使用浏览器工具导航网页、点击按钮、填写表单、截图等。"}
        #     # MessagesPlaceholder(variable_name="agent_scratchpad"),
        # ])

        agent = create_agent(self.llm, tools=tools, system_prompt=None)
        # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # 执行任务
        result = agent.invoke({
            "messages": ["打开 https://www.baidu.com，截图，告诉我前3条新闻的标题"]
        })
        print(result["output"])
    def start(self):
        # 调用模型

        # agent = create_agent(
        #     self.llm, system_prompt="你是一个浏览器自动化助手，可以使用浏览器工具导航网页、点击按钮、填写表单、截图等。",
        #     tools=[collect_leads] + tools
        # )

        # logger.info("开始收集 ...")
        # async for mode, chunk in agent.astream(
        #     {"messages": ["收集储能情报"]}, stream_mode=["updates", "custom", "messages"]
        # ):
        #     if mode == "messages":
        #         # 逐字输出模型回复
        #         if chunk[0].content:
        #             print(chunk[0].content, end="",  flush=True)
        #     elif mode == "updates":
        #         # 输出 Agent 步骤状态
        #         print({"event": "status", "data": str(chunk)})
        #     elif mode == "custom":
        #         # 输出进度信息
        #         print({"event": "progress", "data": chunk})
        # print()
        # logger.info("收集结束 ...")


        logger.info("调用模型: {}", CONF.collector.openai_base_url)

        # prompt = ChatPromptTemplate.from_template("我有哪些工具或者SKIL")
        # parser = StrOutputParser()
        # chain = prompt | self.agent | parser

        logger.info("开始收集 ...")
        for mode, chunk in self.agent.stream(
            {"messages": ["收集储能情报"]}, stream_mode=["updates", "custom", "messages"]
        ):
            if mode == "messages":
                # 逐字输出模型回复
                if chunk[0].content:
                    print(chunk[0].content, end="",  flush=True)
            elif mode == "updates":
                # 输出 Agent 步骤状态
                print({"event": "status", "data": str(chunk)})
            elif mode == "custom":
                # 输出进度信息
                print({"event": "progress", "data": chunk})
        print()
        logger.info("收集结束 ...")


MANAGER = CollectorManager()
