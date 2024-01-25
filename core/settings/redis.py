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


class RedisPubSubService:
    __CONNECT_POINT = aioredis.from_url("redis://localhost")

    def __init__(self):
        self.pubsub = self.__CONNECT_POINT.pubsub()

    async def publish(self, channel: str, message: str):
        await self.__CONNECT_POINT.publish(channel, message)

    async def subcribe(self, room: str):
        await self.pubsub.subscribe(room)
        return self.pubsub

    async def unsub(self, room):
        await self.pubsub.unsubscribe(room)

    async def listen(self):
        while True:
            message = await self.pubsub.subscribe()
            if message is not None and message["type"] == "message":
                for channel, callback in self.subscriptions:
                    if message["channel"] == channel.name:
                        callback(message["data"])

    @property
    def get_connect(self):
        return self.__CONNECT_POINT


redis = RedisPubSubService()
