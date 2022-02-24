from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm_api import views


router = DefaultRouter()
router.register(r'employee', views.EmployeeViewSet)
router.register(r'client', views.ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
