import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import DatabaseSettings

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings
        self._engine = create_async_engine(settings.get_dsn())
        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False
        )

    async def shutdown(self) -> None:
        await self._engine.dispose()
        logger.info("Database manager stopped.")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()
                raise
