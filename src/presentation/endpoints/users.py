from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from src.presentation.schemes.user_schemes import (InviteEmployee,
                                                   RegisterEmployeeScheme)
from src.services.admin_service import AdminService

user_router = APIRouter()


@user_router.post("/generate-invite-token", status_code=202)
async def invite_employee(
    data: InviteEmployee,
    background: BackgroundTasks,
    service: Annotated[AdminService, Depends()],
):
    return await service.generate_invitation_link(data, background)


@user_router.get("/register/{token}", status_code=200)
async def check_token(token: str, service: AdminService = Depends()):
    return await service.check_registration_token(token)


@user_router.post("/register/{token}", status_code=201)
async def check_token(
    token: str,
    data: RegisterEmployeeScheme,
    service: Annotated[AdminService, Depends()],
):
    return await service.register_employee(token, data)
