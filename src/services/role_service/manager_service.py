from passlib.context import CryptContext

from src.repositories.user_repository import UserRepository


class ManagerService:
    def __init__(self) -> None:
        self.crud = UserRepository()
