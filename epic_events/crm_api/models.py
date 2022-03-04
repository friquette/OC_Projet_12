from django.db import models
from django.core.validators import RegexValidator

from employees.models import Employee

PHONE_VALIDATOR = RegexValidator(r"^\+?1?\d{8,15}$")


class Assignee(models.Model):
    date = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related"
    )

    class Meta:
        abstract = True


class EventAssignation(Assignee):
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='event_assignation'
    )


class ContractAssignation(Assignee):
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        related_name='contract_assignation'
    )


class ClientAssignation(Assignee):
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='client_assignation'
    )
    is_converted = models.BooleanField()
    medium = models.CharField(max_length=100)


class DatedItem(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(DatedItem):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(
        validators=[PHONE_VALIDATOR],
        max_length=16,
        unique=True
    )
    mobile = models.CharField(
        validators=[PHONE_VALIDATOR],
        max_length=16,
        unique=True,
        blank=True
    )
    company_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)


class Contract(DatedItem):
    is_signed = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    client_fk = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name="client_contract"
    )


class Event(DatedItem):
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    event_fk = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        related_name="contract_event"
    )
