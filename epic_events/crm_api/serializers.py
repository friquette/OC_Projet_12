from rest_framework import serializers
from crm_api.models import Employee, Client


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}


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
