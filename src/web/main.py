from fastapi import FastAPI

from src.presentation.endpoints.users import user_router
from src.presentation.endpoints.patients import patient_router

app = FastAPI()


app.include_router(user_router)
app.include_router(patient_router)
