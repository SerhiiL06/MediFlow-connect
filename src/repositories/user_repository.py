from core.models.users import User, Specialty
from core.models.records import Record
from .crud_repository import SQLAchemyRepository
from core.settings.connections import session
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException


class UserRepository(SQLAchemyRepository):
    model = User

    async def update_doctor(self, user_id: int, specialty: str):
        async with session() as conn:
            user = await conn.execute(
                select(User)
                .options(selectinload(User.specialties))
                .where(User.id == user_id)
            )

            user = user.scalar_one()

            specialty = await conn.execute(
                select(Specialty).where(Specialty.title == specialty)
            )
            try:
                user.specialties.append(specialty.scalar_one())

                await conn.commit()

            except Exception:
                await conn.rollback()
                raise HTTPException(
                    status_code=400, detail="Doctor already have this specialty"
                )

    async def get_doctor_with_specialty(self, specialty: str) -> User:
        async with session() as conn:
            select(User).where(User.specialties)


class RecordRepository(SQLAchemyRepository):
    model = Record
