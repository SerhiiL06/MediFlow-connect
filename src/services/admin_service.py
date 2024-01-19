from core.settings.redis import RedisTools
from core.settings.main import settings
from itsdangerous import URLSafeSerializer
from src.services.email_service import EmailService


class AdminService:
    def __init__(self):
        self.token = URLSafeSerializer(settings.SECRET_KEY, salt="activate")
        self.redis = RedisTools()
        self.email = EmailService()

    async def generate_invitation_link(self, data) -> dict:
        token = self.token.dumps({"email": data.email})

        await self.redis.set_user_info(
            data.email, data.first_name, data.last_name, role="manager"
        )

        await self.email.send_invation_link(data.email, token)

        return {"message": "link was send", "code": "SEND"}
