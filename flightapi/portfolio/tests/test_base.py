import json
import os

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from portfolio.api.views import FastPaceUserViewSet
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
            password='1234'
        )
        response = self.client.post(url, data=login_payload, format='json')
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

class TestFastPaceUser(APITestCase):

    def setUp(self):
        self.user1 = UserFactory(
            first_name='segun',
            last_name='mathews',
            email='segun@gmail.com',
            password='1234',
            is_staff=True
        )
        self.user2 = UserFactory(
            first_name='taiwo',
            last_name='adedotun',
            email='taiwo@gmail.com',
            password='1234',
        )
        self.user3 = UserFactory(
            first_name='kunle',
            last_name='gold',
            email='kunle@gmail.com',
            password='1234',
        )
        valid_payload = {
            "email": 'segun@gmail.com',
            "password": '1234'
        }
        self.factory = APIRequestFactory()

        self.admin = login_user(valid_payload)
        self.non_admin = login_user(dict(email=self.user3.email, password="1234"))

    def test_list_all_admin(self):
        url = reverse('users-list')
        view = FastPaceUserViewSet.as_view(
            actions={
                'get': 'list',
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin.data['token']))
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'segun')
        self.assertEqual(response.data[0]['email'], 'segun@gmail.com')

    def test_list_non_admin(self):
        url = reverse('users-list')
        view = FastPaceUserViewSet.as_view(
            actions={
                'get': 'list',
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not authorized to view this information')

    def test_get_user_by_id(self):
        url = reverse('users-detail', args=(self.user3.pk,))
        view = FastPaceUserViewSet.as_view(
            actions={
                'get': 'retrieve',
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin.data['token']))

        response = view(request, pk=self.user3.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'kunle')
        self.assertEqual(response.data['email'], 'kunle@gmail.com')
    
    def test_successful_user_update(self):
        url = reverse('users-detail', args=(self.user3.pk,))
        view = FastPaceUserViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(first_name='Imisioluwa'), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request, pk=str(self.user3.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Imisioluwa')

    def test_unsuccessful_user_update(self):
        url = reverse('users-detail', args=(self.user3.pk,))
        view = FastPaceUserViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(first_name='segun'), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request, pk=str(self.user2.pk))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not authorized to update this information')
    
    def test_unsuccessful_user_update_field_not_allowed(self):
        url = reverse('users-detail', args=(self.user2.pk,))
        view = FastPaceUserViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(email='imisioluwa.com'), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request, pk=str(self.user2.pk))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not authorized to update this information')

    def test_upload_photo_successful(self):
        url = reverse('users-upload')
        view = FastPaceUserViewSet.as_view(
            actions={
                'put': 'upload'
            }
        )
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image = os.path.join(base_dir, 'portfolio_photos/photo1.jpg')

        request = self.factory.put(url, data=dict(file=image), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_delete_photo_successful(self):
        url = reverse('users-delete-photo')
        view = FastPaceUserViewSet.as_view(
            actions={
                'delete': 'delete_photo'
            }
        )
        request = self.factory.delete(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))

        response = view(request)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['message'], 'Profile photo deleted successfully')
    


