from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from crm_api.models import (
    Client,
    Event,
    Contract,
    ClientAssignation,
    ContractAssignation,
    EventAssignation
)


class ClientAssignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAssignation
        fields = [
            'id',
            'date',
            'client',
            'employee',
            'is_converted',
            'medium'
        ]


class CustomClientAssignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAssignation
        fields = [
            'id',
            'date',
            'is_converted',
            'medium'
        ]


class CustomClientSerializer(serializers.ModelSerializer):
    assignation = CustomClientAssignationSerializer()

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'job',
            'date_created',
            'date_updated',
            'assignation'
        ]

    def create(self, validated_data):
        user = self.context.get("request").user
        client_data = validated_data.pop('assignation')
        client = Client.objects.create(**validated_data)
        ClientAssignation.objects.create(client=client, employee=user, **client_data)
        return client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'job',
            'date_created',
            'date_updated',
        ]


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'id',
            'is_signed',
            'amount',
            'payment_due',
            'client_fk',
            'date_created',
            'date_updated'
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'attendees',
            'event_date',
            'notes',
            'event_fk',
            'date_created',
            'date_updated'
        ]



class ContractAssignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractAssignation
        fields = [
            'id',
            'date',
            'employee',
            'contract',
        ]


class EventAssignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAssignation
        fields = [
            'id',
            'date',
            'employee',
            'event',
        ]
