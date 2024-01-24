from src.repositories.CrudRepository import UserRepository


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    async def get_my_info(self, user_id: int):
        return await self.repo.get_my_profile(user_id)
