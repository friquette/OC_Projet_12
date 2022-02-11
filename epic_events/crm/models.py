from django.db import models
from django.core.validators import RegexValidator

TEAM_CHOICES = ['sales', 'support',  'management']
PHONE_VALIDATOR = RegexValidator(r"^\+?1?\d{8,15}$")


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    team = models.Charfield(choices=TEAM_CHOICES, max_length=50)


class Client(models.Model):
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
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField()
    sales_contact = models.ForeignKey('User', on_delete=models.SET_NULL)


class Contract(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField()
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    sales_contact = models.ForeignKey('User', on_delete=models.SET_NULL)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)


class Event(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField()
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    event_status = models.ForeignKey('Contract', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    support_contact = models.ForeignKey('Client', on_delete=models.SET_NULL)
