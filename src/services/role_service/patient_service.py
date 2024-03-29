from src.presentation.schemes.record_schemes import CreateRecordScheme
from core.models.records import Record
from core.settings.redis import RedisPubSubService
import secrets
from random import randint
from src.repositories.RecordRepository import RecordRepository
from src.repositories.CrudRepository import UserRepository

from src.utils.crypt import crypt
from fastapi import HTTPException
import json


class PatientService:
    def __init__(self) -> None:
        self.crud = UserRepository()
        self.repo = RecordRepository()
        self.redis = RedisPubSubService()

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

        record_id = await self.repo.submit_record_with_unregister_user(
            record_to_save, patient_to_save
        )

        data = json.dumps({"email": data.email, "pw": random_pw})

        await self.redis.publish("register", data)

        return record_id

    async def register_record_auth_user(self, data: CreateRecordScheme, user_id: int):
        data_to_save = data.model_dump(exclude=["recommended_time"])

        data_to_save.update({"patient_id": user_id})

        result = await self.repo.create_model(Record, data_to_save)

        return result

    async def get_records(self, user_id):
        filtering_data = {"patient_id": user_id}

        query = await self.repo.record_list(filtering_data)

        return query
