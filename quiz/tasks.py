from channels.layers import get_channel_layer
from dramatiq import actor
from asgiref.sync import async_to_sync


@actor
def start_quiz(pk):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "quiz_{}".format(pk), {"type": "quiz.start"}
    )
