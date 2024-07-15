import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.models.images import ImagesModelIn, ImagesModelOut
from app.service.consts import RESIZED_IMAGE_WIDTH

NOT_FOUND_IMAGE_ID = 404
DEPTH = 900.1
PIXELS = [223] * 200


class TestCRUD:
    image_path = "/api/v1/images"

    @pytest.fixture
    def image_in(self) -> ImagesModelIn:
        return ImagesModelIn(
            depth=DEPTH,
            pixels=PIXELS,
        )

    @pytest.mark.asyncio(scope="session")
    async def test_create_and_read(
        self, client: AsyncClient, image_in: ImagesModelIn
    ):
        response = await client.post(
            self.image_path, json=jsonable_encoder(image_in)
        )

        image = ImagesModelOut(**response.json())
        assert image
        assert len(image.pixels) == RESIZED_IMAGE_WIDTH

        response = await client.get(self.image_path + f"/{image.id}")
        image = ImagesModelOut(**response.json())
        assert image

    @pytest.mark.asyncio(scope="session")
    async def test_read_exception(
        self, client: AsyncClient, image_in: ImagesModelIn
    ):
        response = await client.get(self.image_path + f"/{NOT_FOUND_IMAGE_ID}")
        assert response.status_code == 404
