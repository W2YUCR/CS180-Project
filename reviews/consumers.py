from channels.generic.websocket import AsyncJsonWebsocketConsumer
from typing import override


class ReviewWebSocketConsumer(AsyncJsonWebsocketConsumer):
    @override
    async def connect(self):
        self.user = self.scope["user"]
        self.quiz_pk = self.scope["url_route"]["kwargs"]["deck_pk"]
        await self.accept()
