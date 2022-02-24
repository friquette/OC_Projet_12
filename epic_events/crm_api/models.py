from django.db import models, transaction
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.core.validators import RegexValidator

PHONE_VALIDATOR = RegexValidator(r"^\+?1?\d{8,15}$")


class EmployeeManager(BaseUserManager):
    """
    Creates and saves an Employee with the given email and password
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Invalid email')
        try:
            with transaction.atomic():
                employee = self.model(email=email, **extra_fields)
                employee.set_password(password)
                employee.save(using=self._db)
                return employee
        except Exception:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured user
    model with admin-compliant permissions.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=16)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        return self


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
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


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
