import asyncio
from typing import AsyncGenerator

import pytest
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from app.app import create_app
from app.db.base import Base
from app.settings import Settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def cleanup_db(app: FastAPI, settings: Settings) -> None:
    engine: AsyncEngine = app.state.db_manager._engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
async def test_client(settings: Settings) -> AsyncGenerator[TestClient, None]:
    async with TestClient(application=create_app(settings)) as test_client:
        yield test_client


@pytest.fixture(scope="session")
async def app(test_client: TestClient) -> FastAPI:
    return test_client.application


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app)
    ) as client:
        yield client
