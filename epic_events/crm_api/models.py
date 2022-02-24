from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator

PHONE_VALIDATOR = RegexValidator(r"^\+?1?\d{8,15}$")


class Employee(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


class Assignee(models.Model):
    date = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='employees'
    )


class EventAssignation(Assignee):
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='event'
    )


class ContractAssignation(Assignee):
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        related_name='contract'
    )


class ClientAssignation(Assignee):
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='client'
    )
    is_converted = models.BooleanField()
    medium = models.CharField(max_length=100)


class ManipulationDates(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField()


class Client(ManipulationDates):
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


class Contract(ManipulationDates):
    is_signed = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    client_fk = models.ForeignKey('Client', on_delete=models.CASCADE)


class Event(ManipulationDates):
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    event_fk = models.ForeignKey('Contract', on_delete=models.CASCADE)
