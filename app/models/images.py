from pydantic import BaseModel

from app.models.base import BaseListQueryModel


class ImagesListQueryModel(BaseListQueryModel):
    depth_min: float | None
    depth_max: float | None


class ImagesModelIn(BaseModel):
    depth: float
    pixels: list[int]


class ImagesModelOut(BaseModel):
    id: int
    depth: float
    pixels: list[int]
