import codecs

from fastapi import BackgroundTasks, HTTPException
from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadSignature

from core.settings.main import settings
from core.settings.redis import RedisTools
from src.services.email_service import EmailService

from .manager_service import ManagerService


class AdminService(ManagerService):
    def __init__(self):
        super().__init__()

        self.token = URLSafeSerializer(settings.SECRET_KEY, salt="activate")
        self.redis = RedisTools()
        self.email = EmailService()

    async def generate_invitation_link(self, data, task: BackgroundTasks) -> dict:
        token = self.token.dumps({"email": data.email})

        await self.redis.set_user_info(
            data.email, data.first_name, data.last_name, data.role
        )

        task.add_task(self.email.send_invation_link, data.email, token)

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

        hash_pw = self.crypt.hash(data.password1)

        user_data = await self.redis.get_user_info(email)

        data_to_save = {
            "email": token.get("email"),
            "first_name": codecs.decode(user_data[1]),
            "last_name": codecs.decode(user_data[2]),
            "role": codecs.decode(user_data[0]),
            "hashed_password": hash_pw,
        }

        user_id = await self.crud.create_model(data_to_save)

        await self.redis.clean_arr(email)

        return {"message": "CREATE", "code": "201", "userId": user_id}

    @classmethod
    def load_token_data(self, token: str) -> str:
        try:
            token = self.token.loads(token)

        except BadSignature:
            raise HTTPException(
                status_code=404, detail={"message": "something went wrong"}
            )

        return token.get("email")
