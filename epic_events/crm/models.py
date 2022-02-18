from django.db import models
from django.core.validators import RegexValidator

PHONE_VALIDATOR = RegexValidator(r"^\+?1?\d{8,15}$")


class Employee(models.AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)


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


class Time(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField()


class Client(models.Model, Time):
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


class Contract(models.Model, Time):
    is_signed = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE)


class Event(models.Model, Time):
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    event = models.ForeignKey('Contract', on_delete=models.CASCADE)
