from rest_framework import serializers
from django.contrib.auth.models import Group

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'group'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        employee = Employee.objects.create(**validated_data)
        employee.set_password(validated_data['password'])
        group = Group.objects.get(name=validated_data['group'])
        employee.groups.add(group)
        employee.save()

        return employee
