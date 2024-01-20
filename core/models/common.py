from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

pkid = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

create = Annotated[datetime, mapped_column(server_default=func.now())]


deffalse = Annotated[bool, mapped_column(default=False)]
