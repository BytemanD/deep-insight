from pydantic import BaseModel


class Doc(BaseModel):
    id: str
    name: str
    content: str
