from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Table, Column, ForeignKey
from .base import Base
from typing import List

association_table = Table(
    "doctor_special",
    Base.metadata,
    Column("doctor_id", ForeignKey("users.id"), primary_key=True),
    Column("specialty_id", ForeignKey("specialty.id"), primary_key=True),
)


class Specialty(Base):
    __tablename__ = "specialty"

    title: Mapped[str]

    doctors: Mapped[List["User"]] = relationship(
        secondary=association_table, back_populates="specialties"
    )
