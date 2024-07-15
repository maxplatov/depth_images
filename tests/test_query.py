import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.models.images import ImagesModelIn, ImagesModelOut

DEPTH = 900.3
PIXELS = [224] * 200


class TestQuery:
    image_path = "/api/v1/images"

    @pytest.fixture
    def image_in(self) -> ImagesModelIn:
        return ImagesModelIn(
            depth=DEPTH,
            pixels=PIXELS,
        )

    @pytest.mark.asyncio(scope="session")
    async def test_query(self, client: AsyncClient, image_in: ImagesModelIn):
        response = await client.post(
            self.image_path, json=jsonable_encoder(image_in)
        )

        image = ImagesModelOut(**response.json())
        assert image

        response = await client.get(
            self.image_path, params={"depth_min": DEPTH, "depth_max": DEPTH}
        )

        images_out = [
            ImagesModelOut(**image_out) for image_out in response.json()
        ]
        assert images_out
        assert len(images_out) == 1

        response = await client.get(
            self.image_path, params={"depth_min": DEPTH + 1}
        )

        images_out = [
            ImagesModelOut(**image_out) for image_out in response.json()
        ]
        assert not images_out

    @pytest.mark.asyncio(scope="session")
    async def test_query_exception(self, client: AsyncClient):
        response = await client.get(
            self.image_path, params={"depth_min": 1, "depth_max": 0}
        )
        assert response.status_code == 400
