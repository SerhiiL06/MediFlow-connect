import re
from typing import Literal

from pydantic import (BaseModel, ConfigDict, EmailStr, ValidationError,
                      field_validator)


class InviteEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
    role: Literal["manager", "doctor"]

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
