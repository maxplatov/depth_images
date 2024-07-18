import asyncio
import csv
import json

import aiofiles
import aiohttp
import click
from loguru import logger
from yarl import URL

from app.models.images import ImagesModelIn

DEFAULT_URL = "http://127.0.0.1:8000"
HEADERS = {
    "Content-Type": "application/json",
}

IMAGES_ROUTER = "api/v1/images"
DEPTH_COL_NAME = "depth"
DEFAULT_COL_NAME = "col"
MAX_COL_NUMBER = 201


async def send_request(
    session: aiohttp.ClientSession, payload: dict, app_url: str
):
    await session.post(
        URL(app_url) / IMAGES_ROUTER, headers=HEADERS, data=json.dumps(payload)
    )


async def process_csv(file_path: str, app_url: str):
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(file_path, mode="r") as file:
            reader = csv.DictReader((await file.read()).splitlines())
            tasks = []
            for row in reader:
                depth = row[DEPTH_COL_NAME]
                if depth:
                    pixels = [
                        int(row[DEFAULT_COL_NAME + str(i)])
                        for i in range(1, MAX_COL_NUMBER)
                    ]
                    payload = ImagesModelIn(
                        depth=float(depth), pixels=pixels
                    ).model_dump()

                    tasks.append(send_request(session, payload, app_url))

            try:
                await asyncio.gather(*tasks)
            except Exception as e:
                logger.error(e)
                logger.error("Something went wrong. Try again.")
            else:
                logger.info(f"Successfully upload {len(tasks)} images.")


@click.command
@click.option("--file_path", help="Path to csv file")
@click.option(
    "--app_url", help=f"App url, {DEFAULT_URL} by default", default=DEFAULT_URL
)
def main(file_path: str, app_url):
    asyncio.run(process_csv(file_path, app_url))


if __name__ == "__main__":
    main()
