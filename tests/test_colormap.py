import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.models.images import CustomColormapIn, ImagesModelIn, ImagesModelOut

DEPTH = 900.5
PIXELS = [224] * 150
CUSTOM_COLORS = ["green", "green"]


class TestCustomColormap:
    image_path = "/api/v1/images"

    @pytest.fixture
    def image_in(self) -> ImagesModelIn:
        return ImagesModelIn(
            depth=DEPTH,
            pixels=PIXELS,
        )

    @pytest.mark.asyncio(scope="session")
    async def test_colormap(
        self,
        client: AsyncClient,
        image_in: ImagesModelIn,
    ):
        response = await client.post(
            self.image_path, json=jsonable_encoder(image_in)
        )

        image = ImagesModelOut(**response.json())
        assert image

        response = await client.post(
            self.image_path + f"/{image.id}/apply_colormap",
            json=jsonable_encoder(CustomColormapIn(colors=CUSTOM_COLORS)),
        )

        image = ImagesModelOut(**response.json())
        assert image
        assert len(set(image.pixels)) == 1  # all values the same
