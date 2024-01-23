from .ManagerRepository import ManagerRepository
from core.settings.connections import session
from sqlalchemy import select, func, case

from core.models.users import User
from core.models.records import Record
from sqlalchemy.orm import joinedload


class AdminRepository(ManagerRepository):
    async def list_model(self, role: str = None) -> list[User]:
        async with session() as conn:
            query = select(User)
            if role:
                query = query.where(User.role.in_(role))

            result = await conn.execute(query)
            return result.scalars().all()

    async def retrieve_model(self, user_id: int) -> User | None:
        async with session() as conn:
            query = (
                select(User)
                .where(User.id == user_id)
                .options(
                    joinedload(User.doctor_records),
                    joinedload(User.patient_records),
                    joinedload(User.specialties),
                )
            )

            result = await conn.execute(query)

            return result.unique().scalar_one_or_none()
