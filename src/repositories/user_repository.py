from sqlalchemy import insert, select

from core.models.users import User
from .crud_repository import SQLAchemyRepository
from core.settings.connections import session


class UserRepository(SQLAchemyRepository):
    model = User
