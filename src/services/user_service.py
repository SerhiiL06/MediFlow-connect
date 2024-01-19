from src.repositories.user_repository import UserRepository
from fastapi import HTTPException
from passlib.context import CryptContext


class UserService:
    def __init__(self) -> None:
        self.crud = UserRepository()
        self.crypt = CryptContext(schemes="bcrypt")

    async def add_patient(self, data):
        if data.password1 != data.password2:
            raise HTTPException(
                status_code=400, detail={"message": "password must be the same"}
            )

        data_to_save = data.model_dump(exclude=["password1", "password2"])

        hash_pw = self.crypt.hash(data.password1)
        data_to_save.update({"role": "patient", "hashed_password": hash_pw})
        userId = await self.crud.register_patient(data_to_save)

        return {"message": "CREATE", "code": "200", "detail": userId}
