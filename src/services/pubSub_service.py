from .email_service import EmailService
import codecs
import time
import asyncio
from core.settings.redis import RedisPubSubService
import json

shutdown = asyncio.Event()


class PubSubService:
    def __init__(self):
        self.email = EmailService()
        self.redis = RedisPubSubService()

        self.psub = self.redis.pubsub

    async def subscribe_test(self):
        await self.psub.subscribe("test", "register", "document", "invite")

        while not shutdown.is_set():
            message = await self.psub.get_message(
                ignore_subscribe_messages=True, timeout=10
            )
            if message:
                if codecs.decode(message.get("channel")) == "test":
                    current_email = codecs.decode(message.get("data"))
                    await self.email.send_success_message(current_email)

                    await self.redis.publish("document", current_email)

                elif codecs.decode(message.get("channel")) == "register":
                    cred = json.loads(codecs.decode(message.get("data")))

                    await self.email.send_user_creditables(cred["email"], cred["pw"])

                elif codecs.decode(message.get("channel")) == "invite":
                    data = json.loads(codecs.decode(message.get("data")))
                    await self.email.send_invation_link(
                        data.get("email"), data.get("token")
                    )

                elif message.get("channel").decode("utf-8") == "document":
                    with open("document.txt", "a") as file:
                        data = message.get("data").decode("utf-8")
                        file.writelines(f"{data}\n")

            await asyncio.sleep(0.001)


pb_service = PubSubService()
