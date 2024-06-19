from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from models.images import ImagesListQueryModel, ImagesModelOut

auth_router = APIRouter()


@auth_router.get(
    "/images",
    response_model=list[ImagesModelOut],
    status_code=HTTP_200_OK,
)
def get_images(
    query: ImagesListQueryModel = Depends(),
):
    ...
