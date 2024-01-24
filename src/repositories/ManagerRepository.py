from core.models.users import User, Specialty
from core.models.records import Record
from .RecordRepository import RecordRepository
from core.settings.connections import session
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException


class ManagerRepository(RecordRepository):
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

    async def appoint_doctor(self, doctor_id, record_id):
        async with session() as conn:
            query = (
                update(Record)
                .where(Record.id == record_id)
                .values(doctor_id=doctor_id)
                .returning(Record.id)
            )

            result = await conn.execute(query)

            await conn.commit()

            return result.scalar()

    async def get_doctor_with_specialty(self, specialty: str) -> User:
        async with session() as conn:
            select(User).where(User.specialties)
