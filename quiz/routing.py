# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/quiz/(?P<quiz_pk>[0-9]+)/$", consumers.QuizWebSocketConsumer.as_asgi()),
]
