# quiz/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from typing import override

from decks.models import Deck, Card
from quiz.models import Quiz


class QuizFlowTests(TestCase):
    @override
    def setUp(self):
        self.user = User.objects.create_user(username="u", password= "pw")
        self.client.login(username = "u", password ="pw")

        self.deck = Deck.objects.create(owner=self.user, name="Sample")
        for i in range(3):
            Card.objects.create(deck=self.deck, front=f"Q{i}", back=f"A{i}")

        self.client.post(
            reverse("quiz-create", args=[self.deck.pk]),
            data={"seconds_per_card": 20},
        )
        self.quiz = Quiz.objects.filter(deck=self.deck).latest("pk")

    def test_quiz_progression(self):
        cur = reverse("quiz-current", args=[self.quiz.pk])
        nxt = reverse("quiz-next", args=[self.quiz.pk])

        self.assertEqual(self.client.get(cur).json()["front"], "Q0")

        self.client.post(nxt)
        self.assertEqual(self.client.get(cur).json()["front"], "Q1")

        self.client.post(nxt)  
        self.client.post(nxt)  
        self.assertTrue(self.client.get(cur).json()["finished"])
