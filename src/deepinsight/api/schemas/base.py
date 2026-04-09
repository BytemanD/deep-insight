from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """分页参数"""

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1)

    def parse(self) -> tuple[int, int, dict]:
        """解析分页和过滤参数

        Returns:
            tuple: (offset, limit, filters)
                - offset: 偏移量，用于数据库查询的跳过记录数
                - limit: 限制数量，用于数据库查询的返回记录数
                - filters: 过滤条件字典，排除分页参数和空值
        """
        offset = (self.page - 1) * self.page_size
        limit = self.page_size

        # 获取所有过滤条件（排除分页参数）
        filters = self.model_dump(
            exclude_none=True, exclude_unset=True, mode="json", exclude=["page", "page_size"]
        )

        return offset, limit, filters


class LeadQueryParams(PaginationParams):
    """线索过滤条件"""

    status: str | None = None
    region: str | None = None
    stage: str | None = None
    priority: str | None = None
    name: str | None = None
    type: str | None = None


T = TypeVar("T", bound=BaseModel)


class ListResponse(BaseModel, Generic[T]):
    """列表响应通用格式"""

    items: list[T] = []
    total: int = 0
