# quiz/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from typing import override

from decks.models import Deck, Card
from quiz.models import Quiz
