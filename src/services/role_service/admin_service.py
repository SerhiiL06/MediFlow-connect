from fastapi import BackgroundTasks, HTTPException
from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadSignature

from core.settings.main import settings
from core.settings.redis import RedisTools, RedisPubSubService
from core.models.users import User
from src.services.email_service import EmailService
from src.utils.crypt import crypt
import json
from .manager_service import ManagerService
from src.repositories.AdminRepository import AdminRepository


class AdminService(ManagerService):
    def __init__(self):
        super().__init__()

        self.token = URLSafeSerializer(settings.SECRET_KEY, salt="activate")
        self.redis = RedisTools()
        self.predis = RedisPubSubService()
        self.email = EmailService()
        self.crud = AdminRepository()

    async def generate_invitation_link(self, data) -> dict:
        token = self.token.dumps({"email": data.email})

        check = await self.crud.get_user_by_email(data.email)

        if check:
            raise HTTPException(
                status_code=400,
                detail={"message": "user with this email already exists"},
            )

        await self.redis.set_user_info(
            data.email, data.first_name, data.last_name, data.role, data.phone_number
        )

        await self.predis.publish(
            "invite", json.dumps({"email": data.email, "token": token})
        )

        return {"message": "link was send", "code": "SEND"}

    async def check_registration_token(self, token: str):
        email = self.load_token_data(token)
        exists = await self.redis.get_user_info(email)
        result = (
            {"message": "OK", "code": "200"}
            if exists
            else {"message": "EMPY", "code": "404"}
        )
        return result

    async def register_employee(self, token, data):
        email = self.load_token_data(token)
        if data.password1 != data.password2:
            raise HTTPException(
                status_code=400, detail={"message": "password must be the same"}
            )

        hash_pw = crypt.hash(data.password1)

        user_data = await self.redis.get_user_info(email)

        if not user_data:
            raise HTTPException(
                status_code=404, detail={"message": "data doesnt exists"}
            )

        data_to_save = {
            "email": email,
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "role": user_data.get("role"),
            "phone_number": user_data.get("phone_number"),
            "hashed_password": hash_pw,
        }

        user_id = await self.crud.create_model(User, data_to_save)

        await self.redis.clean_arr(email)

        return {"message": "CREATE", "code": "201", "userId": user_id}

    def load_token_data(self, token: str) -> str:
        try:
            token = self.token.loads(token)

        except BadSignature:
            raise HTTPException(
                status_code=404, detail={"message": "something went wrong"}
            )

        return token.get("email")

    async def update_employee(self, emp_id, data):
        data_to_update = data.model_dump(exclude_none=True)
        return await self.crud.update_employee(emp_id, data_to_update)

    async def delete_user(self, object_id: int):
        return await self.crud.delete_model(object_id)

    async def get_user_list(self, role: str):
        result = await self.crud.list_model(role)

        return result

    async def get_user_info(self, user_id: int):
        result = await self.crud.retrieve_model(user_id)

        if result is None:
            raise HTTPException(
                status_code=404, detail={"message": "User doesnt exists"}
            )

        return result
