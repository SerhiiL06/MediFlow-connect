from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from core.settings.main import sqlsetting

engine = create_async_engine(sqlsetting.get_async_url)


session = async_sessionmaker(engine, class_=AsyncSession)
