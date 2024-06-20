import logging

from sqlalchemy import desc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.base import Base

logger = logging.getLogger(__name__)


class BaseAdapter:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def exec(self, stmt):
        try:
            return await self.db_session.execute(stmt)
        except SQLAlchemyError as e:
            logger.exception(e)

    async def get_all(self, stmt):
        result = await self.exec(stmt) or []
        return result and result.scalars().all()

    async def insert(self, model):
        self.db_session.add(model)
        try:
            await self.db_session.flush()
        except SQLAlchemyError as e:
            logger.error(e)
        await self.db_session.refresh(model)
        return model


class BaseRepository(BaseAdapter):
    def __init__(self, entity: Base, db_session: Session):
        self.entity = entity
        super().__init__(db_session)

    @property
    def select(self):
        return select(self.entity).order_by(desc(self.entity.id))

    async def get_one(self, pk: int):
        result = await self.exec(self.select.where(self.entity.id == pk))
        return result and result.scalars().one()
