from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from typing import override, Optional
from quiz.tasks import quiz_show, quiz_submit
from quiz.models import Quiz, QuizResponse


class QuizWebSocketConsumer(AsyncJsonWebsocketConsumer):
    @override
    async def connect(self):
        self.user = self.scope["user"]
        self.quiz_pk = self.scope["url_route"]["kwargs"]["quiz_pk"]
        self.quiz_channel_group_name = "quiz_{}".format(self.quiz_pk)
        await self.channel_layer.group_add(
            self.quiz_channel_group_name, self.channel_name
        )
        quiz = await Quiz.objects.aget(pk=self.quiz_pk)
        await quiz.users.aadd(self.user)
        await quiz.asave()
        await self.accept()

    @override
    async def receive_json(self, content, **kwargs):
        match content:
            case {"action": "start"}:
                await sync_to_async(quiz_show.send)(self.quiz_pk)
            case {"action": "answer", "answer": answer}:
                await sync_to_async(quiz_submit.send)(
                    self.quiz_pk, self.user.pk, answer
                )

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
        score = 0
        async for response in QuizResponse.objects.select_related("card__card").filter(
            card__quiz_id=self.quiz_pk, user=self.user
        ):
            if response.response == response.card.card.back:
                score += 1

        await self.send_json({"type": "end", "score": score})
