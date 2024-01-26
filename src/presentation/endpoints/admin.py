from fastapi import APIRouter, Depends
from src.services.role_service.admin_service import AdminService
from typing import Annotated
from fastapi import Query, Depends
from core.settings.redis import RedisPubSubService
import json

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


@admin_router.post("/pub")
async def pub_message(message: str, service: Annotated[RedisPubSubService, Depends()]):
    await service.publish("test", message)


@admin_router.delete("/users/{user_id}/delete")
async def delete_user(user_id: int, service: Annotated[AdminService, Depends()]):
    return await service.delete_user(user_id)
