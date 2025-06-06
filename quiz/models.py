# quiz/models.py
from django.db import models
from django.contrib.auth.models import User
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
    users: models.ManyToManyField = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse("quiz-view", kwargs={"pk": self.pk})


class QuizCard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    class Meta:
        ordering = ["index"]

class QuizResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(QuizCard, on_delete=models.CASCADE)
    response = models.TextField()