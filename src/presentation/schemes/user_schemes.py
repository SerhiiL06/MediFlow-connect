from pydantic import BaseModel, EmailStr, ConfigDict


class PatientRegister(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password1: str
    password2: str


class InviteEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
