from core.settings.connections import session
from core.models.users import User
from sqlalchemy import insert


class UserRepository:
    async def register_patient(self, data: dict):
        async with session() as conn:
            query = insert(User).values(**data).returning(User.id)

            result = await conn.execute(query)

            return result.scalar()
