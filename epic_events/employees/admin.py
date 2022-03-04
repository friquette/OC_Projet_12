from django.contrib import admin
from .models import Employee
from crm_api.models import (
    Client,
    Contract,
    Event,
    ClientAssignation,
    ContractAssignation,
    EventAssignation
)


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


admin.site.register(Employee)
admin.site.register(ClientAssignation)
admin.site.register(ContractAssignation)
admin.site.register(EventAssignation)
