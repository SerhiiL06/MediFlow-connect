import re
from typing import Optional


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
    phone_number: str = Field(pattern="0[6-9]{1}[0-9]{8}")
    role: str = Field(min_length=1)

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def normalizate(cls, value: str):
        return value.lower().capitalize()

    @field_validator("email", mode="before")
    @classmethod
    def nozmalizate_email(cls, value: EmailStr):
        return value.lower()

    @field_validator("phone_number", mode="after")
    @classmethod
    def after_phone_number(cls, value):
        formatted = f"{value[0:3]}-{value[3:6]}-{value[6:8]}-{value[8:10]}"

        return formatted


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


class ProfileScheme(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, json_encoders={datetime: datetime.date}
    )

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    join_at: datetime
