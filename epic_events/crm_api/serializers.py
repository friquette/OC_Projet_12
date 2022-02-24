from rest_framework import serializers
from crm_api.models import Employee, ClientAssignation


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email']


class ClientAssignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAssignation
        fields = ['id', 'date', 'employee', 'client', 'is_converted', 'medium']
