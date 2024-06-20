from pydantic import BaseModel, Field


class HTTPErrorModel(BaseModel):
    message: str
    status_code: int


class OrderByModel(BaseModel):
    order_by: str | None = None
    desc: bool = True


class PaginationModel(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=50, ge=1, le=100)

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return self.per_page * (self.page - 1)


class BaseListQueryModel(OrderByModel, PaginationModel):
    pass
