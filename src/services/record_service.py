from src.repositories.RecordRepository import RecordRepository


class RecordService:
    def __init__(self):
        self.crud = RecordRepository()

    async def get_records(self, email: str, role: str, uncomplete=False):
        filtering_data = {}

        # if role == "patient":
        #     filtering_data.update({"users_1.email": email})

        # if role == "doctor":
        #     filtering_data.update({"user_2.email": email})

        return await self.crud.record_list(filtering_data, uncomplete)
