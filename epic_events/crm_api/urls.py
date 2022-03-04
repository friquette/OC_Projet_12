from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm_api import views


router = DefaultRouter()
router.register(r'client', views.ClientViewSet, basename='client')
router.register(r'contract', views.ContractViewSet, basename='contract')
router.register(r'event', views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
