from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('deck-detail', kwargs={ 'pk': self.id })

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={ 'pk': self.id })