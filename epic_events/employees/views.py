from django.contrib.auth.signals import user_logged_in
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny

from employees.models import Employee
from employees.serializers import EmployeeSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'employee': reverse('employee-list', request=request, format=format)
    })


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = Employee.objects.filter(email=email, password=password)
        print(f"USER: {Employee.objects.get(email=email)}")
        if user:
            try:
                user_details = {"name": f"{user.first_name} {user.last_name}"}
                user_logged_in.send(
                    sender=user.__class__,
                    request=request,
                    user=user
                )
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {'error': 'Can not authenticate with the given credentials or \
the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'Please provide an email and a password'}
        return Response(res)
