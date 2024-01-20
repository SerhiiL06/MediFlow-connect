import re
from typing import Literal

from pydantic import (BaseModel, ConfigDict, EmailStr, ValidationError,
                      validator)


class InviteEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
    role: Literal["manager", "doctor"]

    @validator("first_name", "last_name", pre=True, always=True)
    def normalizate_fields(self, value: str):
        return value.lower().capitalize()

    @validator("email", pre=True, always=True)
    def nozmalizate_email(self, value: EmailStr):
        return value.lower()


class RegisterEmployeeScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    password1: str
    password2: str

    @validator("password1", "password2")
    def validate_password(self, value):
        if not re.fullmatch(r"^[A-Za-z0-9]{6,}", value):
            raise ValidationError()

        return value
