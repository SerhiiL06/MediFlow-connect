from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

from .base import Base

association_table = Table(
    "doctor_special",
    Base.metadata,
    Column("doctor_id", ForeignKey("users.id"), primary_key=True),
    Column("specialty_id", ForeignKey("specialty.id"), primary_key=True),
)
