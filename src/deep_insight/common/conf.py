from pydantic import BaseModel
from pystonic.conf import BaseAppConfig


class VectorConfig(BaseModel):
    driver: str = "chromadb"


class ChromaDBConfig(BaseModel):
    path: str = "./data/chromadb"


class AppConfig(BaseAppConfig):
    vector: VectorConfig = VectorConfig()
    chromadb: ChromaDBConfig = ChromaDBConfig()


CONF = AppConfig()
