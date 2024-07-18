import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from app.db.models import Image
from app.models.images import ImagesModelOut
from app.service.consts import DEFAULT_COLOR, PIXEL_8_BIT_SIZE, PIXEL_RGB_SIZE


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


def apply_and_get_colormap(pixels: list[int], colors: list[str]) -> list[int]:
    pixels = np.array(pixels)
    pixel_min = np.min(pixels)
    pixel_max = np.max(pixels)

    if pixel_min == pixel_max:
        normalized_frame = np.full_like(pixels, 0.5, dtype=float)
    else:
        normalized_frame = (pixels - pixel_min) / (pixel_max - pixel_min)

    colors = [DEFAULT_COLOR, colors[0]] if len(colors) == 1 else colors

    cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
    colored_frame = cmap(normalized_frame)
    colored_frame_rgb = (
        colored_frame[:, :PIXEL_RGB_SIZE] * PIXEL_8_BIT_SIZE
    ).astype(np.uint8)
    return np.mean(colored_frame_rgb, axis=1).astype(np.uint8).tolist()
