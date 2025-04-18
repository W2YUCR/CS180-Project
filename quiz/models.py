from django.db import models
from decks.models import Card, Deck


# Create your models here.
class Quiz(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, through="QuizCard")
    index = models.PositiveIntegerField()


class QuizCard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    class Meta:
        ordering = ["index"]
