# decks/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from fsrs_rs_python import FSRS, MemoryState


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
    stability = models.FloatField(default=0.0)
    difficulty = models.FloatField(default=5.0)
    last_reviewed = models.DateTimeField(null=True)
    due = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse("card-detail", kwargs={"pk": self.pk})

    def review(self):
        elapsed_days = (datetime.now(datetime.timezone.utc) - self.last_reviewed).days
        fsrs = FSRS(parameters=DEFAULT_PARAMETERS)
        memory = MemoryState(self.stability, self.difficulty)
        next_state = fsrs.next_states(memory, 0.9, elapsed_days)
        next_state = next_state.good
        interval = max(1, round(next_state.interval))

        self.stability = next_state.memory.stability
        self.difficulty = next_state.memory.difficulty
        self.due = self.last_reviewed + timedelta(days=interval)

        self.save()
