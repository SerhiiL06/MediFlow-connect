from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field
from typing import Optional


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
