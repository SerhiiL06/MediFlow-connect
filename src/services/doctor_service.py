from src.repositories.DoctorRepository import DoctorRepository
from core.models.records import DoctorOpinion
from fastapi import UploadFile


class DoctorService(DoctorRepository):
    def __init__(self):
        self.repo = DoctorRepository()

    async def add_opinion(
        self, record_id: int, user: dict, file, short: str
    ) -> DoctorOpinion:

        await self.check_record(record_id, user.get("user_id"))

        file_to_save = await file.read()
        url = self.save_file(file_to_save, file.filename, user.get("email"))

        data = {"short_opinion": short, "opinion": url, "record_id": record_id}

        new = await self.repo.create_opinion(data)

        return new

    @classmethod
    def save_file(cls, file, filename, email) -> str:
        with open(f"media/{email}/{filename}", "wb+") as result:
            result.write(file)

            file_url = f"media/{email}/{filename}"
            return file_url
