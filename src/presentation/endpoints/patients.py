from fastapi import APIRouter
from src.services.role_service.patient_service import PatientService
from src.presentation.schemes.record_schemes import CreateRecordScheme
from fastapi import Depends
from typing import Annotated

patient_router = APIRouter()


@patient_router.post("/create-record")
async def create_record(
    data: CreateRecordScheme, service: Annotated[PatientService, Depends()]
):
    return await service.register_record(data)
