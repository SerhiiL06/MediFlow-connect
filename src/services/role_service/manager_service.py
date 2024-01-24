from core.models.records import Record
from src.repositories.ManagerRepository import ManagerRepository
from src.repositories.RecordRepository import RecordRepository
from fastapi import HTTPException


class ManagerService:
    def __init__(self) -> None:
        self.crud = ManagerRepository()
        self.records = RecordRepository()

    async def update_doctor(self, doctor_id, specialty):
        return await self.crud.update_doctor(doctor_id, specialty)

    async def get_records_list(self):
        return await self.crud.get_record_list()

    async def get_ucomlete(self):
        return await self.records.uncomplete_records()

    async def get_user_records(self):
        return await self.crud.record_list()

    async def retrieve_record(self, record_id: int, user_id: int, role: str):
        result = self.crud.get_record_list()
        if (
            role in ["admin", "manager"]
            or user_id == result.patient_id
            or user_id == result.doctor_id
        ):
            return result

        return HTTPException(
            status_code=404, detail={"message": "object doesnt exists"}
        )

    async def to_appoint_doctor(self, record_id: int, doctor_id: str):
        return await self.crud.appoint_doctor(doctor_id, record_id)
