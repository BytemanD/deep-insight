"""Database Configuration"""

from pydantic import BaseModel
from pystonic.conf import BaseAppConfig


class APISettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DBSettings(BaseModel):
    """Database configuration settings"""

    # Connection URL
    # SQLite: sqlite:///augur.db
    # MySQL: mysql://${user}:${password}@${host}:${port}/${database}
    connection: str = "sqlite:///./data/deepinsight.db"

    # Connection components (used when connection is not explicitly set)
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "root"

    database: str = "deepinsight"
    charset: str = "utf8mb4"

    # Connection pool settings
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False

    @property
    def url(self) -> str:
        """Get database connection URL"""
        return self.connection.format(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    @property
    def async_url(self) -> str:
        """Get async database connection URL"""
        if self.connection.startswith("mysql"):
            return self.connection.replace("mysql://", "mysql+aiomysql://")
        elif self.connection.startswith("sqlite"):
            return self.connection.replace("sqlite://", "sqlite+aiosqlite://")
        return self.connection


class InsightSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001

    openai_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    openai_api_key: str = ""
    openai_model: str = "qwen-plus"

    batch_size: int = 5
    max_concurrent: int = 5


class CollectorSettings(BaseModel):
    openai_base_url: str = ""
    openai_api_key: str = ""
    model: str = ""


class GraphSettings(BaseModel):
    """知识图谱配置"""

    host: str = "0.0.0.0"
    port: int = 8002
    data_dir: str = "data"


class AppSettings(BaseAppConfig):
    """Application settings"""

    db: DBSettings = DBSettings()
    api: APISettings = APISettings()

    collector: CollectorSettings = CollectorSettings()
    insight: InsightSettings = InsightSettings()
    graph: GraphSettings = GraphSettings()

    @property
    def openai_api_key(self) -> str:
        return self.insight.openai_api_key

    @property
    def openai_model(self) -> str:
        return self.insight.openai_model


# Global settings instance
CONF = AppSettings.new()
