from types import MethodType
from typing import override
from datetime import timedelta

from asgiref.sync import async_to_sync
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from decks.models import Deck, Card
from reviews.consumers import ReviewWebSocketConsumer


class ReviewConsumerTests(TestCase):
    @override
    def setUp(self) -> None:
        self.user = User.objects.create_user("u", password="p")
        self.deck = Deck.objects.create(owner=self.user, name="demo", description="d")
        self.consumer = ReviewWebSocketConsumer()
        self.consumer.deck = self.deck

    def test_get_random_card_returns_due(self) -> None:
        past = timezone.now() - timedelta(hours=1)
        due_card = Card.objects.create(deck=self.deck, front="due", back="A", due=past)

        self.consumer.get_random_card()
        self.assertEqual(self.consumer.card, due_card)

    def test_send_next_emits_end_when_empty(self) -> None:
        messages: list[dict[str, str]] = []

        async def fake_send_json(self, payload: dict[str, str]) -> None:
            messages.append(payload)

        def fake_get_random_card(self) -> None:
            self.card = None

        self.consumer.send_json = MethodType(fake_send_json, self.consumer)  # type: ignore
        self.consumer.get_random_card = MethodType(fake_get_random_card, self.consumer)  # type: ignore

        async_to_sync(self.consumer.send_next)()
        self.assertEqual(messages[0]["type"], "end")
