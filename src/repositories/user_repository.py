from sqlalchemy import insert

from core.models.users import User
from core.settings.connections import session


class UserRepository:
    async def register_employee(self, data: dict):
        async with session() as conn:
            query = insert(User).values(**data).returning(User.id)

            result = await conn.execute(query)

            await conn.commit()
            return result.scalar()
