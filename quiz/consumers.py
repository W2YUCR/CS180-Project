from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from typing import override, Optional
from quiz.tasks import start_quiz


class QuizWebSocketConsumer(AsyncJsonWebsocketConsumer):
    @override
    async def connect(self):
        self.quiz_pk = self.scope["url_route"]["kwargs"]["quiz_pk"]
        self.quiz_channel_group_name = "quiz_{}".format(self.quiz_pk)
        await self.channel_layer.group_add(
            self.quiz_channel_group_name, self.channel_name
        )
        await self.accept()

    @override
    async def receive_json(self, content):
        match content:
            case {"action": "start"}:
                await sync_to_async(start_quiz.send)(self.quiz_pk)

    async def quiz_start(self, event):
        print("Received start signal")