from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies import get_images_service
from app.models.images import (
    ImagesListQueryModel,
    ImagesModelIn,
    ImagesModelOut,
)
from app.service.images import ImagesService

images_router = APIRouter()


@images_router.get(
    "/images",
    response_model=list[ImagesModelOut],
    status_code=HTTP_200_OK,
)
async def get_images(
    query: ImagesListQueryModel = Depends(),
    images_service: ImagesService = Depends(get_images_service),
):
    return await images_service.get_all(query)


@images_router.get(
    "/images/{image_id}",
    response_model=ImagesModelOut,
    status_code=HTTP_200_OK,
)
async def get_image(
    image_id: int, images_service: ImagesService = Depends(get_images_service)
):
    return await images_service.get(image_id)


@images_router.post(
    "/images",
    response_model=ImagesModelOut,
    status_code=HTTP_200_OK,
)
async def add_image(
    image: ImagesModelIn,
    images_service: ImagesService = Depends(get_images_service),
):
    return await images_service.create(image)
