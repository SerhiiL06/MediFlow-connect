from fastapi import APIRouter, Depends
from src.services.role_service.admin_service import AdminService
from typing import Annotated
from fastapi import Query, Depends
from core.settings.redis import RedisPubSubService
from src.presentation.common.permission import check_role

from src.services.auth_service import current_user

admin_router = APIRouter(prefix="/admin")


@admin_router.get("/users", tags=["users"])
@check_role(["admin"])
async def user_list(
    user: current_user,
    service: Annotated[AdminService, Depends()],
    role: list[str] = Query(None),
):
    return await service.get_user_list(role)


@admin_router.get("/users/{user_id}", tags=["users"])
@check_role(["admin"])
async def get_user_info(
    user: current_user, user_id: int, service: Annotated[AdminService, Depends()]
):
    return await service.get_user_info(user_id)


@admin_router.post("/pub")
async def pub_message(message: str, service: Annotated[RedisPubSubService, Depends()]):
    await service.publish("test", message)


@admin_router.delete("/users/{user_id}/delete", tags=["users"])
@check_role(["admin"])
async def delete_user(
    user: current_user, user_id: int, service: Annotated[AdminService, Depends()]
):
    return await service.delete_user(user_id)
