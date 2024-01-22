from .CrudRepository import SQLAchemyRepository
from core.settings.connections import session
from sqlalchemy import insert
from core.models.records import Record
from core.models.users import User


class RecordRepository(SQLAchemyRepository):
    async def submit_record_with_unregister_user(
        self, record_data: dict, patient_data: dict
    ):
        async with session() as conn:
            user_query = insert(User).values(**patient_data).returning(User.id)

            result = await conn.execute(user_query)
            record_data.update({"patient_id": result.scalar()})
            record_query = (
                insert(Record)
                .values(**record_data)
                .returning(Record.id)
                .returning(Record.id)
            )

            record = await conn.execute(record_query)

            await conn.commit()

            return record.scalar()
