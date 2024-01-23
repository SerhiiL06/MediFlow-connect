from .CrudRepository import SQLAchemyRepository
from core.settings.connections import session
from sqlalchemy import insert, select, text, func
from sqlalchemy.orm import aliased, joinedload
from core.models.records import Record
from core.models.users import User


class RecordRepository(SQLAchemyRepository):
    async def record_list(self, filtering_data: dict, uncomplete=False) -> list[Record]:
        async with session() as conn:
            doctor_alias = aliased(User)
            patient_alias = aliased(User)
            if not uncomplete:
                query = (
                    select(
                        Record.id,
                        Record.description,
                        func.concat(
                            doctor_alias.last_name + " " + doctor_alias.first_name
                        ).label("doctor_info"),
                        doctor_alias.email.label("doctor_email"),
                        patient_alias.email.label("patient_email"),
                        func.concat(
                            patient_alias.last_name + " " + patient_alias.first_name
                        ).label("patient_info"),
                    )
                    .join(doctor_alias, Record.doctor_id == doctor_alias.id)
                    .join(patient_alias, Record.patient_id == patient_alias.id)
                    .filter(**filtering_data)
                )

                result = await conn.execute(query)

                return result.mappings().all()

            else:
                query = (
                    select(
                        Record.id,
                        Record.description,
                        Record.created_at,
                        User.first_name.label("patient_name"),
                        User.last_name.label("patient_surname"),
                    )
                    .where(Record.doctor_id == None)
                    .join(User, Record.patient_id == User.id)
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
            record_query = insert(Record).values(**record_data).returning(Record.id)

            record = await conn.execute(record_query)

            await conn.commit()

            return record.scalar()
