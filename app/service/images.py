from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.db.models import Image
from app.models.images import (
    ImagesListQueryModel,
    ImagesModelIn,
    ImagesModelOut,
)
from app.repository.images import ImagesRepository


def pixels_transform_to_binary(pixels: list[int]) -> bytearray:
    return bytearray(pixels)


def pixels_transform_from_binary(pixels: bytearray) -> list[int]:
    return list(pixels)


class ImagesService:
    def __init__(self, images_repository: ImagesRepository):
        self._images_repository = images_repository

    async def get(self, image_id: int) -> Image:
        image = await self._images_repository.get_one(image_id)
        if not image:
            raise HTTPException(
                HTTP_404_NOT_FOUND, f"Image with {image_id} not found"
            )
        image.pixels = pixels_transform_from_binary(image.pixels)
        return image

    async def create(self, image: ImagesModelIn) -> Image:
        image.pixels = pixels_transform_to_binary(image.pixels)
        return await self._images_repository.insert(Image(**image.model_dump()))

    async def get_all(
        self, query: ImagesListQueryModel
    ) -> list[ImagesModelOut]:
        images = await self._images_repository.get_all(query)
        images_out_list = []
        for image in images:
            image.pixels = pixels_transform_from_binary(image.pixels)
            images_out_list.append(ImagesModelOut(**image.dict()))
        return images
