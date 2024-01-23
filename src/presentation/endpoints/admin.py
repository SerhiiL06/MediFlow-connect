from fastapi import APIRouter, Depends
from src.services.role_service.admin_service import AdminService
from typing import Annotated, Literal, Optional, Union
from fastapi import Query


admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("/users")
async def user_list(
    service: Annotated[AdminService, Depends()],
    role: list[str] = Query(None),
):
    return await service.get_user_list(role)


@admin_router.get("/users/{user_id}")
async def get_user_info(user_id: int, service: Annotated[AdminService, Depends()]):
    return await service.get_user_info(user_id)
