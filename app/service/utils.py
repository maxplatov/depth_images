import numpy as np

from app.db.models import Image
from app.models.images import ImagesModelOut


def pixels_transform_to_binary(pixels: list[int]) -> bytearray:
    return bytearray(pixels)


def pixels_transform_from_binary(pixels: bytearray) -> list[int]:
    return list(pixels)


def resize_image_width(pixels: list[int], new_size: int) -> list[int]:
    new_pixels = np.linspace(0, len(pixels) - 1, new_size)
    new_pixels = np.interp(new_pixels, np.arange(len(pixels)), pixels)
    return [int(value) for value in new_pixels]


def get_image_out_model(image: Image) -> ImagesModelOut:
    image.pixels = pixels_transform_from_binary(image.pixels)
    return ImagesModelOut.from_orm(image)
