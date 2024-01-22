from src.repositories.DoctorRepository import DoctorRepository


class DoctorService:
    def __init__(self):
        self.repository = DoctorRepository()

    async def list_of_records(self, doctor_id):
        filter_data = {"doctor_id": doctor_id}
        return await self.repository.list_model(filter_data)

    async def retrieve_record(self, doctor_id: int, record_id: int):
        return await self.repository.retrieve_model(doctor_id, record_id)

    def upload_conclusion(self):
        pass
