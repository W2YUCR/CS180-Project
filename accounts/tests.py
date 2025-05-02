from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from typing import override

class SignUpViewTests(TestCase):
    @override
    def setUp(self):
        self.url = reverse('signup')

    def test_signup_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
