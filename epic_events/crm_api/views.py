from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import DjangoModelPermissions

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
        'employee': reverse('employee-list', request=request, format=format),
        'client': reverse('client-list', request=request, format=format)
    })


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [DjangoModelPermissions]

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        client_assignation = ClientAssignation()

        if serializer.is_valid():
            serializer.save()

            client = Client.objects.get(id=serializer.data['id'])
            client_assignation.client = client
            client_assignation.employee = self.request.user
            client_assignation.is_converted = False
            client_assignation.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        user = self.request.user
        client_assignations = ClientAssignation.objects.filter(
            employee=user.id
        )
        queryset = Client.objects.filter(pk__in=[
            client_assignation.client.id for client_assignation in client_assignations
        ])
        firstname = self.request.query_params.get('firstname')
        email = self.request.query_params.get('email')
        if firstname:
            queryset = queryset.filter(first_name__icontains=firstname)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        client_assignations = ClientAssignation.object.filter(
            employee=self.request.user.id
        )
        queryset = Contract.objects.filter(client_fk__in=[
            client.client.id for client in client_assignations
        ])
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
