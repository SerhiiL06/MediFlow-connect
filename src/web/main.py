from fastapi import FastAPI

from src.presentation.endpoints.users import user_router

app = FastAPI()


app.include_router(user_router)
