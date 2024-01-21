from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from src.presentation.schemes.user_schemes import InviteEmployee, RegisterEmployeeScheme
from src.services.role_service.admin_service import AdminService
from src.services.auth_service import AuthService, current_user
from fastapi.security import OAuth2PasswordRequestForm


user_router = APIRouter(prefix="/users")


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


@user_router.post("/token")
async def generate_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends()],
):
    return await service.create_token(form)


@user_router.get("/current")
async def get_currrent(user: current_user):
    return user
