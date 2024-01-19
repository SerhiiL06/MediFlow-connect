from fastapi import APIRouter
from src.services.user_service import UserService
from src.services.admin_service import AdminService
from fastapi import Depends, status
from src.presentation.schemes.user_schemes import PatientRegister, InviteEmployee


user_router = APIRouter()


@user_router.post(
    "/patients/create", status_code=status.HTTP_201_CREATED, tags=["Patient"]
)
async def register(data: PatientRegister, service: UserService = Depends()):
    return await service.add_patient(data)


@user_router.post("/generate-invite-token")
async def invite_employee(data: InviteEmployee, service: AdminService = Depends()):
    return await service.generate_invitation_link(data)
