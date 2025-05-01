# decks/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class DeckViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u1', password='pass')
        self.client.login(username='u1', password='pass')

    def test_deck_list_status_code(self):
        resp = self.client.get(reverse('decks'))
        self.assertEqual(resp.status_code, 200)
