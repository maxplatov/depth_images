from pydantic import BaseModel, Field


class BaseCustomModel(BaseModel):
    class Config:
        from_attributes = True


class HTTPErrorModel(BaseCustomModel):
    message: str
    status_code: int


class OrderByModel(BaseCustomModel):
    order_by: str | None = None
    desc: bool = True


class PaginationModel(BaseCustomModel):
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
