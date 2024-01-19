from redis import asyncio as aioredis


class RedisTools:
    __CONNECT_POINT = aioredis.from_url("redis://localhost")

    async def set_user_info(self, email, first_name, last_name, role):
        await self.__CONNECT_POINT.lpush(email, first_name, last_name, role)

    async def get_user_info(self, email):
        return await self.__CONNECT_POINT.lrange(email, 0, 2)

    async def clean_arr(self, email):
        await self.__CONNECT_POINT.delete(email)

    @property
    def redis_config(self):
        return self.__CONNECT_POINT
