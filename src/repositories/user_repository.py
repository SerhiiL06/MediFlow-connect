from sqlalchemy import insert, select

from core.models.users import User
from .crud_repository import AbstractRepository
from core.settings.connections import session


class UserRepository(AbstractRepository):
    async def register_employee(self, data: dict):
        async with session() as conn:
            query = insert(User).values(**data).returning(User.id)

            result = await conn.execute(query)

            await conn.commit()
            return result.scalar()

    async def get_user_by_email(self, email: str) -> User | None:
        async with session() as conn:
            query = select(User).where(User.email == email)

            result = await conn.execute(query)

            return result.scalars().one_or_none()
