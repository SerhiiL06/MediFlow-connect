from abc import ABC
from core.settings.connections import session
from core.models.base import Base
from sqlalchemy import insert
from core.settings.connections import session
from core.models.users import User
from sqlalchemy import select


class AbstractRepository(ABC):
    def create_model(self):
        raise NotImplemented()

    def retrieve_model(self):
        raise NotImplemented()

    def update_model(self):
        raise NotImplemented()

    def delete_model(self):
        raise NotImplemented()

    def get_user_by_email(self):
        raise NotImplemented()


class SQLAchemyRepository(AbstractRepository):
    model = None

    async def create_model(self, data: dict):
        async with session() as conn:
            query = insert(self.model).values(**data).returning(self.model.id)

            result = await conn.execute(query)

            await conn.commit()

            return result.scalar()

    async def get_user_by_email(self, email: str) -> User | None:
        async with session() as conn:
            query = select(User).where(User.email == email)

            result = await conn.execute(query)

            return result.scalars().one_or_none()
