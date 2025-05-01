from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from typing import override, Optional
from quiz.tasks import quiz_show


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
                await sync_to_async(quiz_show.send)(self.quiz_pk)

    async def quiz_timeout(self, event):
        await self.send_json({"type": "timeout", "answer": event["answer"]})

    async def quiz_show(self, event):
        await self.send_json(
            {
                "type": "show",
                "question": event["question"],
                "end_time": event["end_time"],
            }
        )

    async def quiz_end(self, event):
        await self.send_json({"type": "end"})
