from fastapi import HTTPException
from sqlalchemy import Select
from starlette.status import HTTP_404_NOT_FOUND

from app.db.models import Image
from app.models.images import (
    ImagesListQueryModel,
    ImagesModelIn,
    ImagesModelOut,
)
from app.repository.images import ImagesRepository
from app.service.consts import RESIZED_IMAGE_WIDTH
from app.service.utils import (
    apply_and_get_colormap,
    get_image_out_model,
    pixels_transform_to_binary,
    resize_image_width,
)


class ImagesService:
    def __init__(self, images_repository: ImagesRepository):
        self._images_repository = images_repository

    @staticmethod
    def _get_filtered_query(
        db_query: Select,
        query: ImagesListQueryModel,
    ) -> Select:
        if query.depth_min:
            db_query = db_query.where(Image.depth >= query.depth_min)
        if query.depth_max:
            db_query = db_query.where(Image.depth <= query.depth_max)
        return db_query

    async def get(self, image_id: int) -> ImagesModelOut:
        image = await self._images_repository.get_one(image_id)
        if not image:
            raise HTTPException(
                HTTP_404_NOT_FOUND, f"Image with id={image_id} not found"
            )
        return get_image_out_model(image)

    async def create(self, image: ImagesModelIn) -> ImagesModelOut:
        pixels = resize_image_width(image.pixels, RESIZED_IMAGE_WIDTH)
        image.pixels = pixels_transform_to_binary(pixels)
        new_image = await self._images_repository.create(
            Image(**image.model_dump())
        )
        return get_image_out_model(new_image)

    async def get_all(
        self, query: ImagesListQueryModel
    ) -> list[ImagesModelOut]:
        db_query = self._images_repository.get_select_query(query)
        images = await self._images_repository.get_all(
            self._get_filtered_query(db_query, query)
        )
        images_out_list = []
        for image in images:
            images_out_list.append(get_image_out_model(image))
        return images_out_list

    async def apply_custom_colormap(
        self, image_id: int, colors: list[str]
    ) -> ImagesModelOut:
        image = await self.get(image_id)
        image.pixels = apply_and_get_colormap(image.pixels, colors)
        return image
