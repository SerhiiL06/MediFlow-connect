from fastapi import FastAPI
import asyncio

from src.presentation.endpoints.users import user_router
from src.presentation.endpoints.records import record_router
from src.presentation.endpoints.admin import admin_router
from core.settings.redis import RedisPubSubService
import time
import codecs
from src.services.email_service import EmailService

app = FastAPI()


app.include_router(user_router)
app.include_router(record_router)
app.include_router(admin_router)


shutdown = asyncio.Event()


async def sub_and_lister():
    pub = RedisPubSubService()
    email = EmailService()
    psub = pub.pubsub
    await psub.subscribe("test")

    while not shutdown.is_set():
        message = await psub.get_message(ignore_subscribe_messages=True)
        if message:
            current_email = codecs.decode(message.get("data"))
            await email.send_success_message(current_email)

        time.sleep(0.001)


@app.on_event("startup")
async def listent():
    asyncio.create_task(sub_and_lister())


@app.on_event("shutdown")
async def stop():
    shutdown.set()
