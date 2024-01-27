from typing import Annotated

from fastapi import APIRouter, Depends

from src.presentation.schemes.user_schemes import (
    InviteEmployee,
    RegisterEmployeeScheme,
    EmployeeUpdateScheme,
    ProfileScheme,
    DoctorScheme,
)
from src.presentation.common.permission import check_role
from src.utils.roles import STAFF, AUTHENTICATED
from src.services.role_service.admin_service import AdminService
from src.services.user_service import UserService
from src.services.auth_service import AuthService, current_user
from fastapi.security import OAuth2PasswordRequestForm


user_router = APIRouter(prefix="/users")


@user_router.post(
    "/generate-invite-token",
    summary="Generate information about the new employee. Doctor or manager only and send invitation link.",
    tags=["register"],
    status_code=202,
)
@check_role([STAFF])
async def invite_employee(
    data: InviteEmployee,
    service: Annotated[AdminService, Depends()],
):
    return await service.generate_invitation_link(data)


@user_router.get(
    "/register/{token}", summary="The user", tags=["register"], status_code=200
)
async def check_token(token: str, service: AdminService = Depends()):
    return await service.check_registration_token(token)


@user_router.post("/register/{token}", tags=["register"], status_code=201)
async def create_employee(
    token: str,
    data: RegisterEmployeeScheme,
    service: Annotated[AdminService, Depends()],
):
    return await service.register_employee(token, data)


@user_router.post("/token", tags=["auth"])
async def generate_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends()],
):
    return await service.create_token(form)


@user_router.put("/employees/{emp_id}/", tags=["users"])
@check_role(STAFF)
async def update_doctor(
    emp_id: int,
    data: EmployeeUpdateScheme,
    service: Annotated[AdminService, Depends()],
):
    return await service.update_employee(emp_id, data)


@user_router.get("/me", tags=["users"], response_model=ProfileScheme)
@check_role(AUTHENTICATED)
async def get_me(user: current_user, service: Annotated[UserService, Depends()]):
    return await service.get_my_info(user.get("user_id"))


@user_router.get("/doctors", tags=["users"], response_model=list[DoctorScheme])
@check_role(STAFF)
async def doctors(user: current_user, service: Annotated[UserService, Depends()]):
    return await service.get_doctor_list()


@user_router.get("/patients", tags=["users"])
@check_role(STAFF)
async def patients(user: current_user, service: Annotated[UserService, Depends()]):
    return await service.get_patient_list()
