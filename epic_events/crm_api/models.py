from django.db import models
from django.core.validators import RegexValidator

from employees.models import Employee

PHONE_VALIDATOR = RegexValidator(r"^\+?1?\d{8,15}$")


class Assignee(models.Model):
    date = models.DateField(auto_now=True)
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

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} - {self.event.contract.client.company_name} - {self.date}'  # noqa


class ContractAssignation(Assignee):
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        related_name='contract_assignation'
    )

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} - {self.contract.client.company_name} - {self.date}'  # noqa


class ClientAssignation(Assignee):
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='client_assignation'
    )
    is_converted = models.BooleanField()
    medium = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} - {self.client.company_name}'  # noqa


class DatedItem(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

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
        blank=True
    )
    company_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.company_name}'


class Contract(DatedItem):
    is_signed = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateField()
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name="client_contract"
    )

    def __str__(self):
        return f'{self.client.company_name} - {self.payment_due}'


class Event(DatedItem):
    attendees = models.IntegerField()
    event_date = models.DateField()
    notes = models.TextField()
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        related_name="contract_event"
    )

    def __str__(self):
        return f'{self.contract.client.company_name} - {self.event_date}'
