from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomEmployeeCreationForm, CustomEmployeeChangeForm
from .models import Employee
from crm_api.models import (
    Client,
    Contract,
    Event,
    ClientAssignation,
    ContractAssignation,
    EventAssignation
)


class CustomEmployeeAdmin(UserAdmin):
    add_form = CustomEmployeeCreationForm
    form = CustomEmployeeChangeForm
    model = Employee
    list_display = ['email', 'group']
    list_filter = ['email', 'group']
    fieldsets = (
        ('Employee info', {
            'fields': ('first_name', 'last_name', 'email', 'password')
        }),
        ('Permissions', {'fields': (
            'groups',
            'user_permissions',
            'group',
            'is_staff',
            'is_active',
        )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'group',
                'is_staff',
                'is_active'
            )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    search_fields = [
        'client_fk__first_name',
        'client_fk__last_name',
        'client_fk__email',
        'date_created',
        'amount'
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = [
        'event_fk__client_fk__last_name',
        'event_fk__client_fk__last_name',
        'event_fk__client_fk__email',
        'event_date'
    ]


admin.site.register(Employee, CustomEmployeeAdmin)
admin.site.register(ClientAssignation)
admin.site.register(ContractAssignation)
admin.site.register(EventAssignation)
