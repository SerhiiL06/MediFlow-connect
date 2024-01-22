from fastapi import APIRouter, Request
from src.services.role_service.patient_service import PatientService
from src.services.role_service.manager_service import ManagerService
from src.services.auth_service import current_user
from src.presentation.schemes.record_schemes import (
    CreateRecordScheme,
    SimplyRecordScheme,
    ReadRecordScheme,
)
from fastapi import Depends
from typing import Annotated

record_router = APIRouter()


@record_router.post("/create-record")
async def create_record(
    data: CreateRecordScheme, service: Annotated[PatientService, Depends()]
):
    return await service.register_record(data)


@record_router.post("/register-create-record")
async def submit_record(
    user: current_user,
    data: SimplyRecordScheme,
    service: Annotated[PatientService, Depends()],
):
    return await service.register_record_auth_user(data, user.get("user_id"))


@record_router.get(
    "/records", response_model=list[ReadRecordScheme], response_model_exclude_none=True
)
async def record_list(
    user: current_user, service: Annotated[PatientService, Depends()]
):
    return await service.get_records(user.get("user_id"), user.get("role"))


@record_router.put("/records/{record_id}/appoint-doctor")
async def appoint_doctor(
    record_id: int, doctor_id: int, service: Annotated[ManagerService, Depends()]
):
    return await service.to_appoint_doctor(record_id, doctor_id)
