import math
from typing import Any, List

from django.db.models import QuerySet
from ninja import Field, Schema
from ninja.pagination import PaginationBase



class PageNumberPagination(PaginationBase):
    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(20, ge=1)

    class Output(Schema):
        items: List[Any]
        count: int
        page_count: int

    def __init__(
        self, max_page_size: int = 100, **kwargs: Any
    ) -> None:
        self.max_page_size = max_page_size
        super().__init__(**kwargs)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        page_size = pagination.page_size
        if page_size > self.max_page_size:
            raise ValueError(f"page_size should be less than {self.max_page_size}")
        offset = (pagination.page - 1) * page_size
        count = self._items_count(queryset)
        return {
            "items": queryset[offset : offset + page_size],
            "count": count,
            "page_count": math.ceil(count / page_size),
        }  # noqa: E203
