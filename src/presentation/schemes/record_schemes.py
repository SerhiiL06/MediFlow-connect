from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field
from .user_schemes import DefaultUserListSchema
from typing import Optional
from datetime import datetime


class CreateRecordScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = Field(None, pattern="0[6-9]{1}[0-9]{8}")
    description: str
    recommended_time: str

    @field_validator("phone_number", mode="after")
    @classmethod
    def after_phone_number(cls, value):
        formatted = f"{value[0:3]}-{value[3:6]}-{value[6:8]}-{value[8:10]}"

        return formatted


class SimplyRecordScheme(BaseModel):
    description: str


class ReadRecordScheme(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, json_encoders={datetime: datetime.date}
    )
    description: str
    created_at: datetime
    patient_id: int
    doctor_id: Optional[int] = None


class UncompleteRecord(BaseModel):
    id: int
    created_at: datetime = Field(serialization_alias="register_date")
    description: str
    patient: DefaultUserListSchema
