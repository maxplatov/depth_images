from sqlalchemy import Column, Integer, Float, LargeBinary

from app.db.base import Base


class Image(Base):
    """Images table."""
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    depth = Column(Float, nullable=False, index=True)
    pixels = Column(LargeBinary, nullable=False)
