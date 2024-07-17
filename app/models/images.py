from fastapi import HTTPException
from matplotlib.colors import CSS4_COLORS
from pydantic import Field, model_validator
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


class CustomColormapIn(BaseCustomModel):
    colors: list[str] = Field(
        description="List of colors. For example ['red', 'blue', 'green']"
    )

    @model_validator(mode="after")
    def check_colors(self):
        for color in self.colors:
            if color not in CSS4_COLORS:
                raise HTTPException(
                    HTTP_400_BAD_REQUEST,
                    f"{color} is undefined. Try another one.",
                )
        return self
