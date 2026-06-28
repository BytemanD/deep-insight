# from deepinsight.common.config import CONF
import logging

from langchain.agents import create_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.DEBUG)


class CollectorSettings(BaseModel):
    openai_base_url: str = ""
    openai_api_key: str = ""
    model: str = ""


class AppSettings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter=".",
        extra="ignore",
    )
    collector: CollectorSettings = CollectorSettings()


CONF = AppSettings()

# 1. 创建异步浏览器实例
from langchain_community.tools.playwright.utils import create_async_playwright_browser

async_browser = create_async_playwright_browser()

# 2. 使用异步浏览器参数
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)

# 3. 获取异步工具列表
tools = toolkit.get_tools()
# 现在 tools 中的每个工具都已正确绑定了异步浏览器，可以安全调用

llm = ChatOpenAI(
    base_url=CONF.collector.openai_base_url,
    api_key=CONF.collector.openai_api_key,  # API密钥
    model=CONF.collector.model,
    temperature=0.7,  # 随机性（0-1，越高越随机）
    max_tokens=500,  # 最大输出长度
    timeout=60,  # 请求超时（秒）
    max_retries=2,  # 失败重试次数
)
# print(self.collect_leads())
agent = create_agent(
    llm,
    system_prompt="你是一个专业的情报收集助手",
    tools=tools,
)

result = agent.invoke({"messages": ["打开 https://www.baidu.com，告诉我前3条新闻的标题"]})
print(result["output"])
