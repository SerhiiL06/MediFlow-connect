from fastapi import FastAPI

from src.presentation.endpoints.users import user_router
from src.presentation.endpoints.records import record_router
from src.presentation.endpoints.admin import admin_router

app = FastAPI()


app.include_router(user_router)
app.include_router(record_router)
app.include_router(admin_router)
