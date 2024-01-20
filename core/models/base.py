from sqlalchemy.orm import DeclarativeBase, Mapped

from .common import pkid


class Base(DeclarativeBase):
    id: Mapped[pkid]
