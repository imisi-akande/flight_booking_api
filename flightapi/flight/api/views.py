from django.shortcuts import get_object_or_404
from flight.api.serializers import FlightSerializer, TicketSerializer
from flight.models import Flight, Ticket
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from flight.permissions import IsOwner
from flight.utils import convert_date_to_unix

# Create your views here.

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_permissions(self):
        """
        Set and get permissions for the flight view.
        """
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create', 'destroy', 'update',
                           'partial_update', 'flight_status'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'])
    def flight_status(self, request, pk=None):
        status = request.data.get('status')
        if not status:
            response = dict(message="Status field cannot be empty")
            return Response(response, status=400)

        if status not in (Flight.STATUSES):
            response = dict(message="flight status is incorrect")
            return Response(response, status=400)

        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=pk)

        flight.status = request.data.get('status')
        flight.save()
        serializer = FlightSerializer(flight)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        user = request.user
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            response = dict(message="Flight does not exist")
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if Ticket.objects.filter(user=user, flight=flight).exists():
            return Response(dict(message="Ticket already exist for this flight"), status=409)

        ticket = Ticket.objects.create(
            user=user,
            flight=flight,
            arrival_time=flight.arrival_time,
            arrival_date=flight.arrival_date,
            departure_time=flight.departure_time,
            departure_date=flight.departure_date,
            departure_location=flight.departure_location,
            arrival_location=flight.arrival_location
        )
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=pk)
        ticket = Ticket.objects.filter(user=request.user, flight=flight).exclude(
            status__in=(
                Ticket.RESERVED
            ))
        if ticket.exists():
            response = dict(
                message="This flight has either being booked or confirmed"
            )
            return Response(response, status=400)

        ticket = Ticket.objects.create(
            user=request.user,
            flight=flight,
            arrival_time=flight.arrival_time,
            arrival_date=flight.arrival_date,
            departure_time=flight.departure_time,
            departure_date=flight.departure_date,
            departure_location=flight.departure_location,
            arrival_location=flight.arrival_location,
            status=Ticket.BOOKED
        )
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='reserved/(?P<date>[0-9_-]+)')
    def reserved(self, request, pk=None, date=None):
        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=pk)

        reserved_tickets = flight.tickets.filter(
            status=Ticket.CONFIRMED,
        )
        date_to_timestamp = convert_date_to_unix(date)
        tickets = [
            ticket for ticket in reserved_tickets
            if convert_date_to_unix(ticket.confirmed_from.strftime('%Y-%m-%d')) == date_to_timestamp
        ]

        serializer = TicketSerializer(tickets, many=True)
        response = {
            "reservations": serializer.data,
            "reservations_count": len(tickets)
        }
        return Response(response, status=status.HTTP_200_OK)



class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
