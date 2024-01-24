from fastapi import HTTPException
from redis import asyncio as aioredis


class RedisTools:
    __CONNECT_POINT = aioredis.from_url("redis://localhost")

    async def set_user_info(self, email, first_name, last_name, role, phone_number):
        result = await self.get_user_info(email)

        if result:
            await self.clean_arr(email)

        await self.__CONNECT_POINT.lpush(
            email, first_name, last_name, role, phone_number
        )

    async def get_user_info(self, email):
        data = await self.__CONNECT_POINT.lrange(email, 0, 3)

        return data

    async def clean_arr(self, email):
        await self.__CONNECT_POINT.delete(email)

    @property
    def redis_config(self):
        return self.__CONNECT_POINT


class RedisPubSubManager:
    __CONNECT_POINT = aioredis.from_url("redis://localhost")

    async def connect(self):
        self.pubsub = self.__CONNECT_POINT.pubsub()

    async def publish(self, room: str, message: str):
        await self.__CONNECT_POINT.publish(str, message)

    async def subcribe(self, room: str):
        await self.pubsub.subscribe(room)
        return self.pubsub

    async def unsub(self, room):
        await self.pubsub.unsubscribe(room)
