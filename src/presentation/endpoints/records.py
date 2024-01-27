from fastapi import APIRouter
from src.services.role_service.patient_service import PatientService
from src.services.record_service import RecordService
from src.services.role_service.manager_service import ManagerService
from src.services.auth_service import current_user
from src.presentation.schemes.record_schemes import (
    CreateRecordScheme,
    SimplyRecordScheme,
)

from fastapi import Depends
from typing import Annotated
from src.utils.roles import AUTHENTICATED, ONLY_WORKERS, STAFF
from src.presentation.common.permission import check_role

record_router = APIRouter()


@record_router.post(
    "/create-record",
    summary="Endpoint for UNREGISTER users for create record",
    tags=["records"],
)
async def create_record(
    data: CreateRecordScheme, service: Annotated[PatientService, Depends()]
):
    return await service.register_record(data)


@record_router.post(
    "/register-create-record",
    summary="Endpoint for REGISTER users for create record",
    tags=["records"],
)
@check_role(["patient"])
async def submit_record(
    user: current_user,
    data: SimplyRecordScheme,
    service: Annotated[PatientService, Depends()],
):
    return await service.register_record_auth_user(data, user.get("user_id"))


@record_router.get(
    "/records",
    tags=["records"],
    response_model_exclude_none=True,
)
@check_role(AUTHENTICATED)
async def record_list(
    user: current_user,
    service: Annotated[RecordService, Depends()],
    email: str = None,
):
    return await service.get_records(user.get("user_id"), user.get("role"), email)


@record_router.get(
    "/records/uncomplete",
    tags=["records"],
)
async def uncomplete_orders(
    user: current_user, service: Annotated[RecordService, Depends()]
):
    return await service.get_records(
        user.get("user_ud"), user.get("role"), uncomplete=True
    )


@record_router.get("/records/{record_id}", tags=["records"])
async def get_record_info(
    user: current_user, record_id: int, service: Annotated[RecordService, Depends()]
):
    return await service.retrieve_record(record_id, user)


@record_router.put("/records/{record_id}/appoint-doctor", tags=["records"])
@check_role(STAFF)
async def appoint_doctor(
    record_id: int, doctor_id: int, service: Annotated[ManagerService, Depends()]
):
    return await service.to_appoint_doctor(record_id, doctor_id)
