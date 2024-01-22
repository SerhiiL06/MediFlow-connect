from passlib.context import CryptContext

from src.repositories.ManagerRepository import ManagerRepository


class ManagerService:
    def __init__(self) -> None:
        self.crud = ManagerRepository()

    async def update_doctor(self, doctor_id, specialty):
        return await self.crud.update_doctor(doctor_id, specialty)

    async def get_records_list(self):
        return await self.crud.list_model()

    async def to_appoint_doctor(self, record_id: int, doctor_id: str):
        return await self.crud.appoint_doctor(doctor_id, record_id)
