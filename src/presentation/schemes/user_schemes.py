import re
from typing import Literal, Optional, Union, Any


from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    ValidationError,
    field_validator,
    Field,
)
from datetime import datetime


class InviteEmployee(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, json_encoders={datetime: datetime.date}
    )

    email: EmailStr
    first_name: str
    last_name: str
    role: str

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def normalizate(cls, value: str):
        return value.lower().capitalize()

    @field_validator("email", mode="before")
    @classmethod
    def nozmalizate_email(cls, value: EmailStr):
        return value.lower()


class RegisterEmployeeScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    password1: str
    password2: str

    @field_validator("password1", "password2", mode="before")
    @classmethod
    def validate_password(cls, value):
        if not re.fullmatch(r"^[A-Za-z0-9]{6,}", value):
            raise ValidationError()

        return value


class EmployeeUpdateScheme(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_numper: Optional[str] = None
    calary: Optional[int] = None


class DefaultUserListSchema(InviteEmployee):
    phone_number: Optional[str] = None
    join_at: datetime = Field(serialization_alias="register_date")


# class UserListScheme(DefaultUserListSchema):
#     doctor_records: Optional[list[ReadRecordScheme]] = Field(
#         None, serialization_alias="d_records"
#     )
#     patient_records: Optional[list[ReadRecordScheme]] = Field(
#         None,
#         serialization_alias="p_records",
#     )
#     specialties: list[SpecialtyScheme]
