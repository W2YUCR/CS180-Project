from channels.generic.websocket import AsyncJsonWebsocketConsumer
from decks.models import Deck, Card
from django.utils import timezone
from fsrs import Rating
from asgiref.sync import sync_to_async
import random
from typing import override, Optional


class ReviewWebSocketConsumer(AsyncJsonWebsocketConsumer):
    card: Optional[Card]

    @override
    async def connect(self):
        self.user = self.scope["user"]
        deck_pk = self.scope["url_route"]["kwargs"]["deck_pk"]
        self.deck = await Deck.objects.select_related("owner").aget(pk=deck_pk)
        if self.deck.owner == self.user:
            await self.accept()

    @override
    async def receive_json(self, content):
        match content:
            case {"action": "ready"}:
                await self.send_next()
            case {"action": "flip"}:
                if self.card is None:
                    return
                await self.send_json({"type": "show", "card": self.card.back})
            case {"action": "rate", "rating": rating}:
                if self.card is None:
                    return
                if rating == "good":
                    await sync_to_async(self.card.review)(Rating.Good)
                else:
                    await sync_to_async(self.card.review)(Rating.Again)
                await self.send_next()

    async def send_next(self):
        await sync_to_async(self.get_random_card)()
        if self.card is not None:
            await self.send_json({"type": "show", "card": self.card.front})
        else:
            await self.send_json({"type": "end"})

    def get_random_card(self):
        # Note: Not exactly very efficient
        cards = list(Card.objects.filter(deck=self.deck, due__lte=timezone.now()).all())

        if len(cards) != 0:
            self.card = random.choice(cards)
            return

        cards = list(Card.objects.filter(deck=self.deck, due=None).all())

        if len(cards) != 0:
            self.card = random.choice(cards)
            return

        self.card = None
