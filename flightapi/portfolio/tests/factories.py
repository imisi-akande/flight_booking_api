import json

import factory
from django.test import Client
from django.urls import reverse

from portfolio.models import User

client = Client()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Sequence(lambda n: 'User #{0}'.format(n))
    email = factory.Sequence(lambda n: 'person{0}@gmail.com'.format(n))
    password = factory.PostGeneration(lambda user, create, extracted: user.set_password(extracted))



def login_user(user_credentials):
    """ create a user in testing environment"""
    url = reverse('login')
    user = client.post(url,
                       data=user_credentials,
                       content_type='application/json')
    return user
