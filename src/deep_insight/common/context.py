import contextvars
from typing import Optional

project_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "project_id", default=None
)
