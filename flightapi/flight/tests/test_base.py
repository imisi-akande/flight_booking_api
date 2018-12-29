import datetime
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from portfolio.tests.factories import login_user, UserFactory
from flight.api.views import FlightViewSet, TicketViewSet
from flight.tests.factories import FlightFactory, TicketFactory
from flight.models import Flight, Ticket

from portfolio.models import User


class TestFlightViewSet(APITestCase):

    def setUp(self):
        self.admin = UserFactory(
            is_staff=True,
            email='imisioluwa.akande@gmail.com',
            password='1234',
        )
        self.user = UserFactory(
            email='sola.smith@gmail.com',
            password='1234'
        )

        users = User.objects.all()

        logged_in_admin = login_user(dict(email=self.admin.email, password='1234'))
        logged_in_user = login_user(dict(email=self.user.email, password='1234'))
        self.admin_token = logged_in_admin.data['token']
        self.user_token = logged_in_user.data['token']

        self.factory = APIRequestFactory()
        self.flight_payload = dict(
            flight_number="KF34R",
            arrival_location="Newyork",
            departure_location="lagos",
            departure_time="10:30",
            arrival_time="7:00",
            arrival_date="2017-11-10",
            departure_date='2017-11-30',
            price=2500
        )

        self.flight = FlightFactory(
            flight_number="KF35Z",
            arrival_location="Germany",
            departure_location="lagos",
            departure_time="10:30",
            arrival_time="7:00",
            arrival_date="2017-11-10",
            departure_date='2017-11-30',
            price=2500
        )

    def test_create_flight_success(self):

        url = reverse('flights-list')
        view = FlightViewSet.as_view(
            actions={
                'post': 'create'
            }
        )

        request = self.factory.post(url, data=self.flight_payload, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['flight_number'], 'KF34R')
        self.assertEqual(response.data['arrival_location'], 'Newyork')
        self.assertEqual(response.data['departure_location'], 'lagos')
        self.assertEqual(response.data['status'], Flight.AVAILABLE)


class TestTicketViewSet(APITestCase):

    def setUp(self):
        self.admin = UserFactory(
            is_staff=True,
            email='imisioluwa.akande@gmail.com',
            password='1234',
        )
        self.user = UserFactory(
            email='sola.smith@gmail.com',
            password='1234'
        )

        logged_in_admin = login_user(dict(email=self.admin.email, password='1234'))
        logged_in_user = login_user(dict(email=self.user.email, password='1234'))
        self.admin_token = logged_in_admin.data['token']
        self.user_token = logged_in_user.data['token']

        self.factory = APIRequestFactory()

        self.flight = FlightFactory(
            flight_number="KF35Z",
            arrival_location="Germany",
            departure_location="lagos",
            departure_time="10:30pm",
            arrival_time="7:00am",
            arrival_date="2017-11-10",
            departure_date='2017-11-30',
            price=2500
        )


    def test_list_ticket_success(self):
        TicketFactory(
            status=Ticket.CONFIRMED,
            flight=self.flight,
            user=self.user
        )
        TicketFactory(
            status=Ticket.CONFIRMED,
            flight=self.flight,
            user=UserFactory()
        )

        url = reverse('tickets-list')
        view = TicketViewSet.as_view(
            actions={
                'get': 'list'
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
