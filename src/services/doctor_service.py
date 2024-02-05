from src.repositories.DoctorRepository import DoctorRepository
from core.models.records import DoctorOpinion
from core.settings.redis import RedisPubSubService


class DoctorService(DoctorRepository):
    def __init__(self):
        self.repo = DoctorRepository()
        self.redis = RedisPubSubService()

    async def add_opinion(
        self, record_id: int, user: dict, file, short: str
    ) -> DoctorOpinion:

        record = await self.check_record(record_id, user.get("user_id"))

        file_to_save = await file.read()
        url = self.save_file(file_to_save, file.filename, user.get("email"))

        data = {"short_opinion": short, "opinion": url, "record_id": record_id}

        opinion = await self.repo.create_opinion(data)

        await self.redis.publish("opinion", record.patient.email)

        return opinion

    @classmethod
    def save_file(cls, file: bytes, filename: str, email: str) -> str:
        with open(f"media/{email}/{filename}", "wb+") as result:
            result.write(file)

            file_url = f"media/{email}/{filename}"
            return file_url
