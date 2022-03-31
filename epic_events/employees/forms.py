from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee


class CustomEmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('email',)


class CustomEmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = ('email',)
