from typing import cast

from fastapi import Request

from app.service.images import ImagesService


async def get_images_service(request: Request) -> ImagesService:
    return cast(ImagesService, request.app.state.image_service)
