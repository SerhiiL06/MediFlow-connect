from src.presentation.schemes.record_schemes import CreateRecordScheme
import secrets
from random import randint
from src.repositories.record_repository import RecordRepository
from src.services.email_service import EmailService
from src.utils.crypt import crypt
from fastapi import HTTPException


class PatientService:
    def __init__(self) -> None:
        self.crud = RecordRepository()
        self.email = EmailService()

    async def register_record(self, data: CreateRecordScheme):
        check_user = await self.crud.get_user_by_email(data.email)

        if check_user:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "User with this email aleready exists",
                    "error": "UNIQUE",
                },
            )
        patient_to_save = data.model_dump(exclude=["description", "recommended_time"])

        number = randint(1, 20)

        random_pw = secrets.token_urlsafe(number)

        patient_to_save.update(
            {"hashed_password": crypt.hash(random_pw), "role": "patient"}
        )

        record_to_save = {"description": data.description}

        record_id = await self.crud.create_model(record_to_save, patient_to_save)

        await self.email.send_user_creditables(data.email, random_pw)

        return record_id
