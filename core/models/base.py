from sqlalchemy.orm import DeclarativeBase, Mapped
from .common import pkid, create
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.settings.main import sqlsetting


engine = create_async_engine(sqlsetting.get_async_url)


session = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    id: Mapped[pkid]
    created_at: Mapped[create]
