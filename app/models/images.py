from pydantic import BaseModel

from models.base import BaseListQueryModel


class ImagesListQueryModel(BaseListQueryModel):
    depth_min: float | None
    depth_max: float | None


class ImagesModelOut(BaseModel):
    depth: float
    pixels: list[int]