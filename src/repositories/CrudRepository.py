from abc import ABC
from core.settings.connections import session
from core.settings.connections import session
from core.models.users import User, Specialty, association_table
from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.orm import selectinload


class AbstractRepository(ABC):
    def create_model(self):
        raise NotImplemented()

    def list_model(self):
        raise NotImplemented()

    def retrieve_model(self):
        raise NotImplemented()

    def update_model(self):
        raise NotImplemented()

    def delete_model(self):
        raise NotImplemented()

    def get_user_by_email(self):
        raise NotImplemented()


class SQLAchemyRepository(AbstractRepository):
    async def create_model(self, model, data: dict):
        async with session() as conn:
            query = insert(model).values(**data).returning(model.id)

            result = await conn.execute(query)

            await conn.commit()

            return result.scalar()

    async def list_model(self, model, filter_data: dict = None):
        async with session() as conn:
            query = select(model)

            if filter_data is not None:
                query = query.filter_by(**filter_data)

            result = await conn.execute(query)

            return result.scalars().all()

    async def retrieve_model(self, model, object_id):
        async with session() as conn:
            query = select(model).where(model.id == object_id)

            result = await conn.execute(query)

            return result.mappings().one_or_none()

    async def update_model(self, model, object_id, data: dict):
        async with session() as conn:
            query = (
                update(model)
                .where(model.id == object_id)
                .values(**data)
                .returning(model.id)
            )

            await conn.execute(query)

            await conn.commit()

            return {"message": "user update"}

    async def delete_model(self, model, object_id):
        async with session() as conn:
            query = delete(model).where(model.id == object_id)

            await conn.execute(query)

            await conn.commit()

            return {"code": 204, "message": "DELETE"}


class UserRepository(AbstractRepository):
    async def get_user_by_email(self, email: str) -> User | None:
        async with session() as conn:
            query = select(User).where(User.email == email)

            result = await conn.execute(query)

            return result.scalars().one_or_none()

    async def get_my_profile(self, user_id: int) -> User:
        async with session() as conn:
            query = select(User).where(User.id == user_id)

            user = await conn.execute(query)

            return user.scalar_one()

    async def get_doctors(self):
        async with session() as conn:
            query = (
                select(User)
                .join(association_table)
                .join(Specialty)
                .filter(User.role == "doctor")
                .options(selectinload(User.specialties))
            )
            result = await conn.execute(query)

            return result.scalars().all()

    async def get_patients(self):
        async with session() as conn:
            info = func.concat(User.first_name + " " + User.last_name).label("USER_FL")
            query = (
                select(User.id, info, User.email, User.phone_number)
                .where(User.role == "patient")
                .order_by(User.join_at.desc())
            )

            result = await conn.execute(query)

            return result.mappings().all()
