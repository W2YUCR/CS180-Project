# decks/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decks.models import Deck, Card
from typing import override


class DeckViewTests(TestCase):
    @override
    def setUp(self):
        self.user = User.objects.create_user("u1", password="pass")
        self.client.login(username="u1", password="pass")

    def test_deck_list_status_code(self):
        resp = self.client.get(reverse("decks"))
        self.assertEqual(resp.status_code, 200)


class DecksTestCase(TestCase):
    @override
    def setUp(self):
        user1 = User.objects.create_user("user 1", password="abc")
        user2 = User.objects.create_user("user 2", password="abc")
        deck = Deck.objects.create(owner=user1, name="user 1 deck")
        shared_deck = Deck.objects.create(
            owner=user1, name="user 1 shared deck", published=True
        )

    def test_user_can_access_own_decks(self):
        deck = Deck.objects.get(name="user 1 deck")
        client = Client()
        self.assertTrue(client.login(username="user 1", password="abc"))
        response = client.get(reverse("deck-detail", kwargs={"pk": deck.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_access_other_private_decks(self):
        deck = Deck.objects.get(name="user 1 deck")
        client = Client()
        self.assertTrue(client.login(username="user 2", password="abc"))
        response = client.get(reverse("deck-detail", kwargs={"pk": deck.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test_user_can_access_other_shared_decks(self):
        deck = Deck.objects.get(name="user 1 shared deck")
        client = Client()
        self.assertTrue(client.login(username="user 2", password="abc"))
        response = client.get(reverse("deck-detail", kwargs={"pk": deck.pk}))
        self.assertEqual(response.status_code, 200)
