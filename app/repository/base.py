from loguru import logger
from sqlalchemy import Select, asc, desc, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.base import Base
from app.db.engine import DatabaseManager
from app.models.base import BaseListQueryModel


class BaseAdapter:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def exec(self, stmt):
        try:
            async with self.db_manager.session() as session:
                return await session.execute(stmt)
        except SQLAlchemyError as e:
            logger.exception(e)

    async def get_all(self, stmt: Select):
        result = await self.exec(stmt) or []
        return result and result.scalars().all()

    async def create(self, model):
        try:
            async with self.db_manager.session() as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
        except SQLAlchemyError as e:
            logger.error(e)
        return model


class BaseRepository(BaseAdapter):
    def __init__(self, entity: Base, db_manager: DatabaseManager):
        self.entity = entity
        super().__init__(db_manager)

    def get_orderby_query(
        self,
        db_query: Select,
        query: BaseListQueryModel,
    ) -> Select:
        order_by = self.entity.id
        if query.order_by:
            order_by = query.order_by
        direction = desc if query.desc else asc
        return db_query.order_by(direction(order_by))

    @staticmethod
    def get_pagination_query(
        db_query: Select,
        query: BaseListQueryModel,
    ) -> Select:
        return db_query.limit(query.limit).offset(query.offset)

    def get_select_query(self, query: BaseListQueryModel) -> Select:
        db_query = select(self.entity)
        db_query = self.get_orderby_query(db_query, query)
        db_query = self.get_pagination_query(db_query, query)
        return db_query

    async def get_one(self, pk: int):
        result = await self.exec(
            select(self.entity).where(self.entity.id == pk)
        )
        return result and result.scalars().first()
