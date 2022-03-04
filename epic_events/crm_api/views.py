from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from crm_api.models import Client, Contract, Event
from crm_api.serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'client': reverse('client-list', request=request, format=format)
    })


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
