from fastapi import FastAPI
from core.settings.connections import session
from core.models.specialty import Specialty
from sqlalchemy import select

app = FastAPI()


@app.get("/")
async def hello():
    async with session() as conn:
        query = select(Specialty)

        result = await conn.execute(query)

        return result.mappings().all()
