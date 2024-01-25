from fastapi import FastAPI
import asyncio

from src.presentation.endpoints.users import user_router
from src.presentation.endpoints.records import record_router
from src.presentation.endpoints.admin import admin_router
from src.services.pubSub_service import pb_service, shutdown

app = FastAPI()


app.include_router(user_router)
app.include_router(record_router)
app.include_router(admin_router)


@app.on_event("startup")
async def listening():
    asyncio.create_task(pb_service.subscribe_test())


@app.on_event("shutdown")
async def stop():
    shutdown.set()
