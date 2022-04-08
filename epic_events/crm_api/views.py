from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Q

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
    CustomClientSerializer,
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
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == "POST":
            serializer_class = CustomClientSerializer
        else:
            serializer_class = ClientSerializer
        return serializer_class

    def get_queryset(self):
        user = self.request.user
        queryset = Client.objects.all()

        if not user.is_superuser:
            if 'Sales' in user.groups():
                client_assignations = ClientAssignation.objects.filter(
                    employee=user.id
                )
                queryset = Client.objects.filter(pk__in=[
                    assignation.client.id for assignation in client_assignations
                ])
            elif 'Support' in user.groups():
                event_assignations = EventAssignation.objects.filter(
                    employee=user.id
                )
                events = Event.objects.filter(pk__in=[
                    assignation.event.id for assignation in event_assignations
                ])
                queryset = Client.objects.filter(pk__in=[
                    event.contract_id.client_id for event in events
                ])

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | Q(email__icontains=search)
            )

        return queryset


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [DjangoModelPermissions]

    def create(self, request):
        serializer = ContractSerializer(data=request.data)
        contract_assignation = ContractAssignation()

        if serializer.is_valid():
            serializer.save()

            contract = Contract.objects.get(id=serializer.data['id'])
            contract_assignation.client = contract
            contract_assignation.employee = self.request.user
            contract_assignation.save()

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
        queryset = Client.objects.all()

        if not user.is_superuser:
            client_assignations = ClientAssignation.objects.filter(
                employee=self.request.user.id
            )
            queryset = Contract.objects.filter(pk__in=[
                assignation.client.id for assignation in client_assignations
            ])

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(client_id__first_name__icontains=search) |
                Q(client_id__email__icontains=search) |
                Q(date_created__icontains=search) |
                Q(amount__icontains=search)
            )

        return queryset


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [DjangoModelPermissions]

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        event_assignation = EventAssignation()

        if serializer.is_valid():
            serializer.save()

            event = Event.objects.get(id=serializer.data['id'])
            event_assignation.event = event
            event_assignation.employee = self.request.user
            event_assignation.save()

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
        queryset = Event.objects.all()

        if not user.is_superuser:
            event_assignations = EventAssignation.objects.filter(
                employee=self.request.user.id
            )
            queryset = Event.objects.filter(pk__in=[
                assignation.client.id for assignation in event_assignations
            ])

        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(event_id__client_id__first_name__icontains=search) |
                Q(event_id__client_id__email__icontains=search) |
                Q(event_date__icontains=search)
            )

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
