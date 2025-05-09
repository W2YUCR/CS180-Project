from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from dramatiq import actor
from asgiref.sync import async_to_sync
from quiz.models import Quiz, QuizCard, QuizResponse
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


@actor
def quiz_submit(pk: int, user_pk: int, answer: str) -> None:
    channel_layer = get_channel_layer()
    quiz = Quiz.objects.get(pk=pk)
    card = QuizCard.objects.get(quiz=quiz, index=quiz.index)
    QuizResponse.objects.create(user_id=user_pk, card=card, response=answer)

    # Check if all users have submitted
    if all(
        QuizResponse.objects.filter(user=user, card=card).exists()
        for user in quiz.users.all()
    ):
        quiz_timeout.send(pk)
