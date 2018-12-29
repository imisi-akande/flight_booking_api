import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField
from flight.mixins import FlightMixin


class Flight(FlightMixin):
    AVAILABLE = 'AVAILABLE'
    DELAYED = 'DELAYED'
    ARRIVED = 'ARRIVED'
    CANCELLED = 'CANCELLED'
    DEPARTED = 'DEPARTED'
    LANDED = 'LANDED'

    STATUS = (
        (AVAILABLE, 'Available'),
        (DELAYED, 'Delayed'),
        (ARRIVED, 'Arrived'),
        (CANCELLED, 'Cancelled'),
        (DEPARTED, 'Departed'),
        (LANDED, 'Landed'),
    )

    STATUSES = (
        AVAILABLE,
        DEPARTED,
        DELAYED,
        CANCELLED,
        LANDED,
        ARRIVED
    )

    flight_number = models.CharField(max_length=255, blank=False)
    status = models.CharField(max_length=50, choices=STATUS, default=AVAILABLE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='NGN')
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Ticket(FlightMixin):
    RESERVED = 'RESERVED'
    BOOKED = 'BOOKED'
    CONFIRMED = 'CONFIRMED'

    STATUS = (
        (RESERVED, 'Reserved'),
        (BOOKED, 'Booked'),
        (CONFIRMED, 'Confirmed'),
    )
    booking_reference = models.CharField(max_length=255, blank=True, null=True)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE, related_name="tickets", null=True)
    status = models.CharField(max_length=50, choices=STATUS, default=RESERVED)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    confirmed_from = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == Ticket.CONFIRMED:
            self.booking_reference = self.reference_id_generator()
            self.confirmed_from = datetime.now(tz=timezone.utc)
        super(Ticket, self).save(*args, **kwargs)

    def reference_id_generator(self):
        return uuid.uuid4().hex.upper()[0:6]
