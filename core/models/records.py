from .base import Base
from .common import create
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Record(Base):
    __tablename__ = "records"
    description: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[create]

    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=True
    )

    patient = relationship(
        "User", back_populates="patient_records", foreign_keys=[patient_id]
    )
    doctor = relationship(
        "User", back_populates="doctor_records", foreign_keys=[doctor_id]
    )


class DoctorOpinion(Base):
    __tablename__ = "doctor_opinions"

    short_opinion: Mapped[str] = mapped_column(comment="The short text opinion")
    opinion: Mapped[str]
    record_id: Mapped[int] = mapped_column(ForeignKey("records.id"))
    created_at: Mapped[create]
