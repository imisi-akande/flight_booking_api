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

    def test_create_flight_non_admin_fail(self):
        url = reverse('flights-list')
        view = FlightViewSet.as_view(
            actions={
                'post': 'create'
            }
        )

        request = self.factory.post(url, data=self.flight_payload, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))
        response = view(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "You do not have permission to perform this action.")

    def test_update_flight_status_success(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, data=dict(status="LANDED"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], Flight.LANDED)

    def test_update_flight_status_non_admin(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, data=dict(status="LANDED"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')  

    def test_no_flight_status_fail(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'],'Status field cannot be empty')

    def test_incorrect_flight_status_fail(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, data=dict(status="EXPIRED"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'],'flight status is incorrect')    

    def test_book_flight_success(self):
        url = reverse('flights-book', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'book'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], Ticket.BOOKED)
        self.assertEqual(response.data['arrival_location'], 'Germany')
        self.assertEqual(response.data['departure_location'], 'lagos')

    def test_book_flight_for_booked_ticket_fail(self):
        TicketFactory(
            status=Ticket.BOOKED,
            flight=self.flight,
            user=self.user
        )

        url = reverse('flights-book', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'book'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'This flight has either being booked or confirmed') 

    def test_reserve_ticket_flight_not_exist(self):
        url = reverse('flights-reserve', args=(23,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserve'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=23)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Flight does not exist')

    def test_tickets_confirmed_for_flight_success(self):
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        TicketFactory(
            status=Ticket.CONFIRMED,
            flight=self.flight,
            user=self.user,
        )
        url = reverse('flights-reserved', args=(self.flight.pk, date))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserved'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))

        response = view(request, pk=self.flight.pk, date=date)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['reservations_count'], 1)    

    def test_reserve_ticket_already_exist(self):
        TicketFactory(
            status=Ticket.BOOKED,
            flight=self.flight,
            user=self.user
        )
        url = reverse('flights-reserve', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserve'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['message'], 'Ticket already exist for this flight')    
     

    def test_reserve_ticket_success(self):
        url = reverse('flights-reserve', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserve'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], Ticket.RESERVED)
        self.assertEqual(response.data['arrival_location'], 'Germany')
        self.assertEqual(response.data['departure_location'], 'lagos')      

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

    def test_book_ticket_success(self):
        ticket = TicketFactory(
            status=Ticket.RESERVED,
            flight=self.flight,
            user=self.user
        )
        url = reverse('tickets-book', args=(ticket.pk,))

        view = TicketViewSet.as_view(
            actions={
                'patch': 'book'
            }
        )
        request = self.factory.patch(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))
        response = view(request, pk=ticket.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], Ticket.BOOKED)

    def test_book_ticket_unauthorized(self):
        ticket = TicketFactory(
            status=Ticket.BOOKED,
            flight=self.flight,
            user=self.user
        )
        url = reverse('tickets-book', args=(ticket.pk,))

        view = TicketViewSet.as_view(
            actions={
                'patch': 'book'
            }
        )

        request = self.factory.patch(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request, pk=ticket.pk)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], "You are not authorized to book this ticket")

    def test_book_ticket_with_status_booked(self):
        ticket = TicketFactory(
        status=Ticket.BOOKED,
        flight=self.flight,
        user=self.user
        )
        url = reverse('tickets-book', args=(ticket.pk,))

        view = TicketViewSet.as_view(
            actions={
                'patch': 'book'
            }
        )

        request = self.factory.patch(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))
        response = view(request, pk=ticket.pk)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['message'], "This ticket has either been booked or purchased")

    def test_purchase_ticket_success(self):
        ticket = TicketFactory(
            status=Ticket.BOOKED,
            flight=self.flight,
            user=self.user
        )
        url = reverse('tickets-purchase', args=(ticket.pk,))

        view = TicketViewSet.as_view(
            actions={
                'post': 'purchase'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))
        response = view(request, pk=ticket.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], Ticket.CONFIRMED)

    def test_purchase_ticket_fail_unauthorized(self):
        ticket = TicketFactory(
        status=Ticket.BOOKED,
        flight=self.flight,
        user=self.user
        )

        url = reverse('tickets-purchase', args=(ticket.pk,))
        view = TicketViewSet.as_view(
            actions={
                'post': 'purchase'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], "You are not authorized to purchase this ticket")

    def test_purchase_ticket_fail_confirmed(self):
        ticket = TicketFactory(
        status=Ticket.CONFIRMED,
        flight=self.flight,
        user=self.user,
        arrival_location="Bayelsa"
        )

        url = reverse('tickets-purchase', args=(ticket.pk,))
        view = TicketViewSet.as_view(
            actions={
                'post': 'purchase'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))
        response = view(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Ticket has been purchased for this flight")

    def test_update_ticket_success(self):
        ticket = TicketFactory(
            status=Ticket.RESERVED,
            flight=self.flight,
            user=self.user
        )

        url = reverse('tickets-detail', args=(ticket.pk,))
        view = TicketViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(arrival_location="lagos"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['arrival_location'], "lagos")

    def test_update_ticket_unauthorized_access(self):
        ticket = TicketFactory(
            status=Ticket.RESERVED,
            flight=self.flight,
            user=self.user
        )

        url = reverse('tickets-detail', args=(ticket.pk,))
        view = TicketViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(arrival_location="lagos"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))

        response = view(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not authorized to update this ticket')
    
    def test_update_ticket_fail_for_booked_and_confirmed(self):
        ticket = TicketFactory(
        status=Ticket.CONFIRMED,
        flight=self.flight,
        user=self.user
    )

        url = reverse('tickets-detail', args=(ticket.pk,))
        view = TicketViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(arrival_location="lagos"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Cannot update a booked or confirmed ticket")

    def test_update_ticket_fail_for_disallowed_field(self):
        ticket = TicketFactory(
            status=Ticket.RESERVED,
            flight=self.flight,
            user=self.user
        )

        url = reverse('tickets-detail', args=(ticket.pk,))
        view = TicketViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(status=Ticket.BOOKED), HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=ticket.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Some of the fields provided are not permitted for this action")