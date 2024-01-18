from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
from typing import Annotated
from datetime import datetime


pkid = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

create = Annotated[datetime, mapped_column(server_default=func.now())]


deffalse = Annotated[bool, mapped_column(default=False)]
