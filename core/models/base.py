from sqlalchemy.orm import DeclarativeBase, Mapped
from .common import pkid, create


class Base(DeclarativeBase):
    id: Mapped[pkid]
    created_at: Mapped[create]
