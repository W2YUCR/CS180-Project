from channels.generic.websocket import WebsocketConsumer
from typing import override


class QuizWebSocketConsumer(WebsocketConsumer):
    @override
    def connect(self):
        print("Connected")
        self.accept()
