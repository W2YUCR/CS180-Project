from channels.layers import get_channel_layer
from dramatiq import actor
from asgiref.sync import async_to_sync
from quiz.models import Quiz
import time


@actor
def quiz_show(pk):
    channel_layer = get_channel_layer()
    quiz = Quiz.objects.get(pk=pk)
    card = quiz.cards.get(quizcard__index=quiz.index)

    async_to_sync(channel_layer.group_send)(
        "quiz_{}".format(pk),
        {
            "type": "quiz.show",
            "question": card.front,
            "end_time": int(time.time_ns() / 1_000_000) + quiz.seconds_per_card * 1000,
        },
    )

    quiz_timeout.send_with_options(args=(pk,), delay=quiz.seconds_per_card * 1000)


@actor
def quiz_timeout(pk):
    channel_layer = get_channel_layer()
    quiz = Quiz.objects.get(pk=pk)
    card = quiz.cards.get(quizcard__index=quiz.index)

    async_to_sync(channel_layer.group_send)(
        "quiz_{}".format(pk), {"type": "quiz.timeout", "answer": card.back}
    )
    quiz_next.send_with_options(args=(pk,), delay=5000)


@actor
def quiz_next(pk):
    channel_layer = get_channel_layer()
    quiz = Quiz.objects.get(pk=pk)

    next_index = quiz.index + 1

    if next_index < quiz.cards.count():
        quiz.index = next_index
        quiz.save()
        quiz_show.send(pk)
    else:
        async_to_sync(channel_layer.group_send)(
            "quiz_{}".format(pk), {"type": "quiz.end"}
        )
