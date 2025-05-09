# quiz/models.py
from django.db import models
from decks.models import Card, Deck
from django.urls import reverse

from typing import override


# Create your models here.
class Quiz(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    seconds_per_card = models.PositiveSmallIntegerField(default=30)
    review_limit = models.PositiveSmallIntegerField(null=True)
    cards: models.ManyToManyField = models.ManyToManyField(Card, through="QuizCard")
    index = models.PositiveIntegerField()

    @override
    def get_absolute_url(self):
        return reverse("quiz-view", kwargs={"pk": self.pk})


class QuizCard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    class Meta:
        ordering = ["index"]
