from .CrudRepository import SQLAchemyRepository
from core.models.records import Record
from core.settings.connections import session
from sqlalchemy import select
from fastapi import HTTPException


class DoctorRepository(SQLAchemyRepository):
    async def retrieve_model(self, doctor_id: int, object_id: int):
        async with session() as conn:
            query = select(Record).where(Record.id == object_id)

            obj = await conn.execute(query)

            if (
                obj.scalar_one_or_none() is None
                or obj.scalar_one_or_none().doctor_id != doctor_id
            ):
                raise HTTPException(
                    status_code=403, detail={"message": "permission danied"}
                )

            return obj
