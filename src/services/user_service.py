from passlib.context import CryptContext

from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self) -> None:
        self.crud = UserRepository()
        self.crypt = CryptContext(schemes="bcrypt")
