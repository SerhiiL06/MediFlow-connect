from decimal import Decimal
from typing import List

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .common import create, deffalse
from .specialty import association_table
from .utils import Roles


class Specialty(Base):
    __tablename__ = "specialty"

    title: Mapped[str]

    doctors: Mapped[List["User"]] = relationship(
        secondary=association_table, back_populates="specialties"
    )


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[str] = mapped_column(Enum(Roles))
    calary: Mapped[Decimal] = mapped_column(default=0)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str]

    join_at: Mapped[create]

    specialties: Mapped[List["Specialty"]] = relationship(
        back_populates="doctors", secondary=association_table
    )

    working_days: Mapped["WorkingDays"] = relationship(back_populates="doctor")
    __table_args__ = (UniqueConstraint("email", "phone_number"),)


class WorkingDays(Base):
    __tablename__ = "working_days"
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    monday: Mapped[deffalse]
    tuesday: Mapped[deffalse]
    wednesday: Mapped[deffalse]
    thursday: Mapped[deffalse]
    friday: Mapped[deffalse]
    saturday: Mapped[deffalse]
    sunday: Mapped[deffalse]

    doctor: Mapped["User"] = relationship(back_populates="working_days")
