from fastapi import WebSocket
from core.settings.redis import RedisPubSubManager


class WebSocketService:
    def __init__(self):
        self.rooms = {}
        self.pubsub = RedisPubSubManager()

    async def subs_to_room(self, room: str, websocket: WebSocket):
        await websocket.accept()

        if room in self.rooms:
            self.rooms[room].append(websocket)

        else:
            self.rooms[room] = [websocket]

            await self.pubsub.connect()
            await self.pubsub.subcribe(room)

    async def publ_to_room(self, room, message):
        await self.pubsub.publish(room, message)

    async def remove_user_from_room(self, room, websocket: WebSocket):
        self.rooms[room].remove(websocket)
        await self.pubsub.unsub(room)
