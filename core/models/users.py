from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint, Table, Column, Enum
from decimal import Decimal
from .utils import Roles
from .common import deffalse


class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]

    role: Mapped[str] = mapped_column(Enum(Roles))

    calary: Mapped[Decimal] = mapped_column(default=0)

    phone_number: Mapped[str] = mapped_column(nullable=True)

    hashed_password: Mapped[str]

    __table_args__ = (UniqueConstraint("email", "phone_number"),)


association_table = Table(
    "doctor_special",
    Base.metadata,
    Column("doctor_id", ForeignKey("users.id"), primary_key=True),
    Column("specialty_id", ForeignKey("specialty.id"), primary_key=True),
)


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


class Specialty(Base):
    __tablename__ = "specialty"

    title: Mapped[str]
