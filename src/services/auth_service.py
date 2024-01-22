import jwt
from fastapi import HTTPException, Depends
from core.settings.main import settings
from src.repositories.ManagerRepository import ManagerRepository
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from src.utils.crypt import crypt
from typing import Annotated


bearer = OAuth2PasswordBearer(tokenUrl="users/token")


class AuthService:
    def __init__(self):
        self.repository = ManagerRepository()

    async def create_token(self, data: OAuth2PasswordRequestForm):
        check_exists = await self.repository.get_user_by_email(data.username)

        if check_exists is None:
            raise HTTPException(
                status_code=403, detail={"error": "user with this email doesnt exists"}
            )

        if not crypt.verify(data.password, check_exists.hashed_password):
            raise HTTPException(status_code=403, detail={"error": "invalid data"})

        exp = datetime.now() + timedelta(minutes=30)
        payload = {
            "email": data.username,
            "user_id": check_exists.id,
            "role": check_exists.role.value,
            "exp": exp,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return {"access_token": token, "token_type": "bearer"}

    def verify_token(self, token):
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        if datetime.now() > datetime.fromtimestamp(data.get("exp")):
            raise HTTPException(status_code=403, detail={"error": "token exp"})

        return data


auth = AuthService()


def authenticated(token: Annotated[str, Depends(bearer)]):
    if token is None:
        raise jwt.PyJWTError()
    return auth.verify_token(token)


current_user = Annotated[dict, Depends(authenticated)]
