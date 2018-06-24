import unittest
from django.test import TestCase, Client


class TestLogin(TestCase):
    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

    def test_login_ok(self):
        self.login_data = {
            'username': 'studente',
            'password': '12345678pw'
        }
        response = self.c.post('/login/', self.login_data, follow=True)
        self.assertTrue(response.context['user'].is_active)