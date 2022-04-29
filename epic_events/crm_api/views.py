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
    CustomEventSerializer,
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
        serializer_class = ClientSerializer

        if self.request.method == "POST":
            serializer_class = CustomClientSerializer

        return serializer_class

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance_serializer = ClientSerializer(request.data)
        return Response(instance_serializer.data)

    def get_queryset(self):
        user = self.request.user
        queryset = Client.objects.all()

        if not user.is_superuser:
            if user.group == 'Sales':
                client_assignations = ClientAssignation.objects.filter(
                    employee=user.id
                )
                queryset = Client.objects.filter(pk__in=[
                    assignation.client.id for assignation in client_assignations  # noqa
                ])
            elif user.group == 'Support':
                event_assignations = EventAssignation.objects.filter(
                    employee=user.id
                )
                events = Event.objects.filter(pk__in=[
                    assignation.event.id for assignation in event_assignations
                ])
                contracts = Contract.objects.filter(
                    pk__in=[event.contract.id for event in events]
                )
                queryset = Client.objects.filter(pk__in=[
                    contract.client.id for contract in contracts
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
            contract_assignation.contract = contract
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
        queryset = Contract.objects.all()

        if not user.is_superuser:
            client_assignations = ClientAssignation.objects.filter(
                employee=user
            )
            queryset = Contract.objects.filter(client__in=[
                assignation.client for assignation in client_assignations
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
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        serializer_class = EventSerializer

        if self.request.method == "POST":
            serializer_class = CustomEventSerializer

        return serializer_class

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance_serializer = EventSerializer(data=request.data)
        instance_serializer.is_valid(raise_exception=True)
        return Response(instance_serializer.data)

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.all()

        if not user.is_superuser:
            event_assignations = EventAssignation.objects.filter(
                employee=user.id
            )
            queryset = Event.objects.filter(pk__in=[
                assignation.event.id for assignation in event_assignations
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

    def get_queryset(self):
        user = self.request.user
        queryset = ClientAssignation.objects.all()

        if not user.is_superuser:
            queryset = ClientAssignation.objects.filter(employee=user)

        return queryset


class ContractAssignationViewSet(viewsets.ModelViewSet):
    queryset = ContractAssignation.objects.all()
    serializer_class = ContractAssignationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ContractAssignation.objects.all()

        if not user.is_superuser:
            queryset = ContractAssignation.objects.filter(employee=user)

        return queryset


class EventAssignationViewSet(viewsets.ModelViewSet):
    queryset = EventAssignation.objects.all()
    serializer_class = EventAssignationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = EventAssignation.objects.all()

        if not user.is_superuser:
            queryset = EventAssignation.objects.filter(employee=user)

        return queryset
