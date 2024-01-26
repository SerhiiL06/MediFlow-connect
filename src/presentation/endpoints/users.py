from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from src.presentation.schemes.user_schemes import (
    InviteEmployee,
    RegisterEmployeeScheme,
    EmployeeUpdateScheme,
    ProfileScheme,
)
from src.services.role_service.admin_service import AdminService
from src.services.user_service import UserService
from src.services.auth_service import AuthService, current_user
from fastapi.security import OAuth2PasswordRequestForm


user_router = APIRouter(prefix="/users")


@user_router.post(
    "/generate-invite-token",
    summary="Generate information about the new employee. Doctor or manager only and send invitation link.",
    tags=["Admin", "Manager"],
    status_code=202,
)
async def invite_employee(
    data: InviteEmployee,
    service: Annotated[AdminService, Depends()],
):
    return await service.generate_invitation_link(data)


@user_router.get(
    "/register/{token}", summary="The user", tags=["Register"], status_code=200
)
async def check_token(token: str, service: AdminService = Depends()):
    return await service.check_registration_token(token)


@user_router.post("/register/{token}", tags=["Register"], status_code=201)
async def create_employee(
    token: str,
    data: RegisterEmployeeScheme,
    service: Annotated[AdminService, Depends()],
):
    return await service.register_employee(token, data)


@user_router.post("/token", tags=["Auth"])
async def generate_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends()],
):
    return await service.create_token(form)


@user_router.put("/employees/{emp_id}/", tags=["Manager", "Admin"])
async def update_doctor(
    emp_id: int,
    data: EmployeeUpdateScheme,
    service: Annotated[AdminService, Depends()],
):
    return await service.update_employee(emp_id, data)


@user_router.get("/me", response_model=ProfileScheme)
async def get_me(user: current_user, service: Annotated[UserService, Depends()]):
    return await service.get_my_info(user.get("user_id"))


@user_router.get("/doctors", tags=["Test"])
async def doctors(service: Annotated[UserService, Depends()]):
    return await service.get_doctor_list()


@user_router.get("/patients", tags=["Test"])
async def patients(service: Annotated[UserService, Depends()]):
    return await service.get_patient_list()
