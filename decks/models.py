# decks/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
import fsrs
from fsrs import Rating

class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description")
    published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("deck-detail", kwargs={"pk": self.pk})


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()
    fsrs = models.JSONField(null=True)
    due = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse("card-detail", kwargs={"pk": self.pk})

    def review(self, rating: Rating) -> None:
        scheduler = fsrs.Scheduler()
        if self.fsrs is None:
            card = fsrs.Card()
        else:
            card = fsrs.Card.from_dict(self.fsrs)
        card, review_log = scheduler.review_card(card, rating)
        self.fsrs = card.to_dict()
        self.due = card.due
        self.save()
