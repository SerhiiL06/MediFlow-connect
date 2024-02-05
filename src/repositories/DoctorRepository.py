from .CrudRepository import SQLAchemyRepository
from core.models.records import Record, DoctorOpinion
from core.settings.connections import session
from sqlalchemy import select, insert
from fastapi import HTTPException


class DoctorRepository(SQLAchemyRepository):
    async def retrieve_model(self, doctor_id: int, object_id: int) -> Record:
        record = await self.check_record(session, object_id, doctor_id)
        return record

    async def create_opinion(self, data: dict):
        async with session() as conn:

            insert_query = insert(DoctorOpinion).values(**data).returning("*")

            result = await conn.execute(insert_query)

            await conn.commit()

            return result.mappings()

    async def check_record(self, record_id: int, doctor_id) -> Record:
        async with session() as conn:
            query = select(Record).where(Record.id == record_id)

            result = await conn.execute(query)

            record = result.scalar_one_or_none()

            if record is None or record.doctor_id != doctor_id:
                raise HTTPException(
                    status_code=403, detail={"message": "permission danied"}
                )

            return record
