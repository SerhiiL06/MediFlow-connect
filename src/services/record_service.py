from src.repositories.RecordRepository import RecordRepository
from fastapi import HTTPException
from src.utils.roles import STAFF


class RecordService:
    def __init__(self):
        self.crud = RecordRepository()

    async def get_records(self, user_id: int, role: str, uncomplete=False):
        filtering_data = {}

        return await self.crud.record_list(filtering_data, role, user_id, uncomplete)

    async def retrieve_record(self, record_id: int, user: dict):
        record = await self.crud.record_detail(record_id)

        if not record:
            raise HTTPException(
                status_code=404, detail={"message": "record doesnt exists"}
            )

        if user.get("role") not in STAFF and (
            record.doctor_id != user.get("user_id")
            or record.patient_id != user.get("user_id")
        ):
            raise HTTPException(
                status_code=401, detail={"message": "permission danied"}
            )

        return record
