from .CrudRepository import SQLAchemyRepository
from core.settings.connections import session
from sqlalchemy import insert, select
from sqlalchemy.orm import aliased
from core.models.records import Record
from core.models.users import User


class RecordRepository(SQLAchemyRepository):
    async def record_list(self):
        async with session() as conn:
            doctor_alias = aliased(User)
            patient_alias = aliased(User)
            query = (
                select(
                    Record.id,
                    Record.description,
                    doctor_alias.email.label("doctor_email"),
                    doctor_alias.last_name.label("doctor_surname"),
                    patient_alias.email.label("patient_email"),
                    patient_alias.last_name.label("patient_surname"),
                )
                .join(doctor_alias, Record.doctor_id == doctor_alias.id)
                .join(patient_alias, Record.patient_id == patient_alias.id)
            )

            result = await conn.execute(query)
            return result.mappings().all()

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
