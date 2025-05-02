# quiz/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from typing import override

from decks.models import Deck, Card
from quiz.models import Quiz

class QuizCreateTest(TestCase):
    @override
    def setUp(self):
        
        self.user = User.objects.create_user("user1", password="pass")
        self.client.login(username="user1", password="pass")
        self.deck = Deck.objects.create(owner=self.user, name="Deck-A")
        Card.objects.create(deck=self.deck, front="Front", back="Back")

    def test_quiz_can_be_created(self):
        response = self.client.post(reverse("quiz-create"), data={"deck_pk": self.deck.pk})
        self.assertEqual(response.status_code, 302)   
        self.assertEqual(Quiz.objects.count(), 1)     
