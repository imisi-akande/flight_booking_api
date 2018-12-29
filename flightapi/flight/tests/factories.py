import factory
import factory.fuzzy
from datetime import datetime, timezone

from flight.models import Flight, Ticket


class FlightFactory(factory.DjangoModelFactory):
    class Meta:
        model = Flight


class TicketFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ticket
