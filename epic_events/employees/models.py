from django.db import models, transaction
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class EmployeeManager(BaseUserManager):
    """
    Creates and saves an Employee with the given email and password
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Invalid email')
        try:
            with transaction.atomic():
                employee = self.model(
                    email=email,
                    password=password,
                    **extra_fields
                )
                employee.set_password(password)
                employee.save(using=self._db)
                return employee
        except Exception:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )


class Employee(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured user
    model with admin-compliant permissions.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=16)

    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        return self
