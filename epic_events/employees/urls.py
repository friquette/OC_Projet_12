from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employees import views


router = DefaultRouter()
router.register(r'employee', views.EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
