from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/reviews/(?P<deck_pk>[0-9]+)/$", consumers.ReviewWebSocketConsumer.as_asgi()),
]
