from rest_framework import serializers
from crm_api.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'date', 'employee', 'client', 'is_converted', 'medium']
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
            'date_updated'
        ]
