from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.models.images import ImagesListQueryModel, ImagesModelOut
from app.api.dependencies import get_images_service
from app.service.images import ImagesService

images_router = APIRouter()


@images_router.get(
    "/images",
    response_model=list[ImagesModelOut],
    status_code=HTTP_200_OK,
)
async def get_images(
    query: ImagesListQueryModel,
    images_service: ImagesService = Depends(get_images_service)
):
    return await images_service.get_all(query)


@images_router.get(
    "/{image_id}",
    response_model=ImagesModelOut,
    status_code=HTTP_200_OK,
)
async def get_image(
    image_id: int,
    images_service: ImagesService = Depends(get_images_service)
):
    return await images_service.get(image_id)
