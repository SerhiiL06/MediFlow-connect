from .CrudRepository import SQLAchemyRepository
from core.settings.connections import session
from sqlalchemy import insert, select, func, or_
from sqlalchemy.orm import aliased
from core.models.records import Record
from core.models.users import User


class RecordRepository(SQLAchemyRepository):
    doctor_alias = aliased(User)
    patient_alias = aliased(User)

    async def record_list(
        self, role: str, user_id: int, filtering_data: dict = None, uncomplete=False
    ) -> list[Record]:
        async with session() as conn:
            doc_info = func.concat(
                self.doctor_alias.last_name + " " + self.doctor_alias.first_name
            ).label("doctor_info")

            pat_info = func.concat(
                self.patient_alias.last_name + " " + self.patient_alias.first_name
            ).label("patient_info")

            if not uncomplete:
                query = (
                    select(
                        Record.id,
                        Record.description,
                        doc_info,
                        self.doctor_alias.email.label("doctor_email"),
                        self.patient_alias.email.label("patient_email"),
                        pat_info,
                    )
                    .join(self.doctor_alias, Record.doctor_id == self.doctor_alias.id)
                    .join(
                        self.patient_alias, Record.patient_id == self.patient_alias.id
                    )
                )

                if role == "doctor":
                    query = query.filter(self.doctor_alias.id == user_id)

                if role == "patient":
                    query = query.filter(self.patient_alias.id == user_id)

                if filtering_data.get("email"):
                    query = query.filter(
                        or_(
                            self.doctor_alias.email == filtering_data.get("email"),
                            self.patient_alias.email == filtering_data.get("email"),
                        )
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

    async def record_detail(self, record_id: int) -> Record:
        doc_info = func.concat(
            self.doctor_alias.first_name + " " + self.doctor_alias.last_name
        ).label("doc_name_surname")

        patient_info = func.concat(
            self.patient_alias.first_name + " " + self.patient_alias.last_name
        ).label("pat_name_surname")

        async with session() as conn:
            query = (
                select(
                    Record.id,
                    Record.description,
                    Record.created_at,
                    doc_info,
                    patient_info,
                )
                .join(self.doctor_alias, Record.doctor_id == self.doctor_alias.id)
                .join(self.patient_alias, Record.patient_id == self.patient_alias.id)
                .where(Record.id == record_id)
            )

            result = await conn.execute(query)

            return result.mappings().one_or_none()

    async def submit_record_with_unregister_user(
        self, record_data: dict, patient_data: dict
    ) -> int:
        async with session() as conn:
            user_query = insert(User).values(**patient_data).returning(User.id)

            result = await conn.execute(user_query)
            record_data.update({"patient_id": result.scalar()})
            record_query = insert(Record).values(**record_data).returning(Record.id)

            record = await conn.execute(record_query)

            await conn.commit()

            return record.scalar()
