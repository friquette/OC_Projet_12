from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class EmployeeManager(BaseUserManager):
    """
    Creates and saves an Employee with the given email and password
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Invalid email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured user
    model with admin-compliant permissions.
    """
    EMPLOYEE_GROUPS = [
        ('Sales', 'Sales'),
        ('Support', 'Support')
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    group = models.CharField(max_length=10, choices=EMPLOYEE_GROUPS)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    def __str__(self):
        return self.email
