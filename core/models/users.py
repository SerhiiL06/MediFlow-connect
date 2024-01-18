from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Enum
from decimal import Decimal
from .specialty import association_table
from .utils import Roles
from .common import deffalse
from typing import List


class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[str] = mapped_column(Enum(Roles))
    calary: Mapped[Decimal] = mapped_column(default=0)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str]

    specialties: Mapped[List["Specialty"]] = relationship(
        secondary="doctors", secondary=association_table
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
