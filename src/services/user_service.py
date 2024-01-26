from src.repositories.CrudRepository import UserRepository


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    async def get_doctor_list(self):
        return await self.repo.get_doctors()

    async def get_patient_list(self):
        return await self.repo.get_patients()

    async def get_my_info(self, user_id: int):
        return await self.repo.get_my_profile(user_id)
