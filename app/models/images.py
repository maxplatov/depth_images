from fastapi import HTTPException
from pydantic import model_validator
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.base import BaseCustomModel, BaseListQueryModel


class ImagesListQueryModel(BaseListQueryModel):
    depth_min: float | None = None
    depth_max: float | None = None

    @model_validator(mode="after")
    def check_depths(self):
        if (
            None not in [self.depth_min, self.depth_max]
            and self.depth_min > self.depth_max
        ):
            raise HTTPException(
                HTTP_400_BAD_REQUEST, "depth_min must be less than depth_max"
            )
        return self


class ImagesModelIn(BaseCustomModel):
    depth: float
    pixels: list[int]


class ImagesModelOut(BaseCustomModel):
    id: int
    depth: float
    pixels: list[int]
