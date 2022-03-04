from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from crm_api.models import (
    Client,
    Contract,
    Event,
    ClientAssignation,
    ContractAssignation,
    EventAssignation
)
from crm_api.serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
    ClientAssignationSerializer,
    ContractAssignationSerializer,
    EventAssignationSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'client': reverse('client-list', request=request, format=format)
    })


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = Client.objects.all()
        firstname = self.request.query_params.get('firstname')
        email = self.request.query_params.get('email')
        if firstname:
            queryset = queryset.filter(first_name__icontains=firstname)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        queryset = Contract.objects.all()
        firstname = self.request.query_params.get('firstname')
        email = self.request.query_params.get('email')
        date = self.request.query_params.get('date')
        amount = self.request.query_params.get('amount')
        if firstname:
            queryset = queryset.filter(
                client_fk__first_name__icontains=firstname
            )
        if email:
            queryset = queryset.filter(client_fk__email__icontains=email)
        if date:
            queryset = queryset.filter(date_created__icontains=date)
        if amount:
            queryset = queryset.filter(amount__icontains=amount)

        return queryset


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        firstname = self.request.query_params.get('firstname')
        email = self.request.query_params.get('email')
        date = self.request.query_params.get('date')

        if firstname:
            queryset = queryset.filter(
                event_fk__client_fk__first_name__icontains=firstname
            )
        if email:
            queryset = queryset.filter(
                event_fk__client_fk__email__icontains=email
            )
        if date:
            queryset = queryset.filter(event_date__icontains=date)

        return queryset


class ClientAssignationViewSet(viewsets.ModelViewSet):
    queryset = ClientAssignation.objects.all()
    serializer_class = ClientAssignationSerializer


class ContractAssignationViewSet(viewsets.ModelViewSet):
    queryset = ContractAssignation.objects.all()
    serializer_class = ContractAssignationSerializer


class EventAssignationViewSet(viewsets.ModelViewSet):
    queryset = EventAssignation.objects.all()
    serializer_class = EventAssignationSerializer
