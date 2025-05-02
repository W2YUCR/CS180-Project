# decks/tests.py
from typing import override
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from typing import override

class DeckViewTests(TestCase):
    @override
    def setUp(self):
        self.user = User.objects.create_user('u1', password='pass')
        self.client.login(username='u1', password='pass')

    def test_deck_list_status_code(self):
        resp = self.client.get(reverse('decks'))
        self.assertEqual(resp.status_code, 200)
