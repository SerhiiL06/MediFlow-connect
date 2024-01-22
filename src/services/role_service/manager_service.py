from passlib.context import CryptContext

from src.repositories.user_repository import UserRepository


class ManagerService:
    def __init__(self) -> None:
        self.crud = UserRepository()

    async def update_doctor(self, doctor_id, specialty):
        return await self.crud.update_doctor(doctor_id, specialty)

    async def get_records_list(self):
        return await self.crud.list_model()

    async def to_appoint_doctor(self, record_id: int, specialty: str):
        self.crud.retrieve_model
