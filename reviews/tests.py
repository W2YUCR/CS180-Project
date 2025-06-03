from types import MethodType

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from asgiref.sync import async_to_sync

from decks.models import Deck, Card
from reviews.consumers import ReviewWebSocketConsumer


class ReviewConsumerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", password="p")
        self.deck = Deck.objects.create(owner=self.user,
                                        name="demo", description="d")
        self.consumer = ReviewWebSocketConsumer()
        self.consumer.deck = self.deck


    def test_get_random_card_returns_due(self):
        past = timezone.now() - timezone.timedelta(hours=1)
        due_card = Card.objects.create(deck=self.deck, front="due",
                                       back="A", due=past)

        self.consumer.get_random_card()
        self.assertEqual(self.consumer.card, due_card)

    def test_send_next_emits_end_when_empty(self):
        messages = []

        async def fake_send_json(self, payload):
            messages.append(payload)

        def fake_get_random_card(self):
            self.card = None

        self.consumer.send_json = MethodType(fake_send_json, self.consumer)
        self.consumer.get_random_card = MethodType(fake_get_random_card, self.consumer)

        async_to_sync(self.consumer.send_next)()
        self.assertEqual(messages[0]["type"], "end")
