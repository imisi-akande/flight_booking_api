import json
import os

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from portfolio.api.views import AirtechUserViewSet
from portfolio.models import User
from portfolio.tests.factories import login_user, UserFactory

client = Client()


class TestUserSignup(TestCase):
    def setUp(self):
        self.user_payload = {
            "first_name": 'sola',
            "last_name": 'smith',
            "email": 'sola.smith@gmail.com',
            "password": "1234"
        }

        self.invalid_payload = {
            "last_name": 'steve',
            "password": "steve"
        }

    def test_successful_signup(self):
        url = reverse('sign_up')
        response = client.post(url,
                               data=json.dumps(self.user_payload),
                               content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'sola.smith@gmail.com')

    def test_unsuccessful_signup(self):
        url = reverse('sign_up')
        response = client.post(url, data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'email, password and firstname are required')


class TestUserLogin(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            first_name='sola',
            last_name='smith',
            email='sola.smith@yahoo.com',
            password='1234'
        )
        self.url = reverse('login')

    def test_successful_login(self):
        url = reverse('login')
        login_payload = dict(
            email=self.user.email,
            password="funky"
        )
        response = self.client.post(url, data=json.dumps(login_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'sola.smith@yahoo.com')

    def test_unsuccessful_login(self):
        invalid_payload = {
            'email': 'charles@y.com',
            'password': 'test123'
        }
        response = client.post(self.url, data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Invalid request')

