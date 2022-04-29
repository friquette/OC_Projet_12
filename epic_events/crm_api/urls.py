from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm_api import views


router = DefaultRouter()
router.register(r'client', views.ClientViewSet, basename='client')
router.register(r'client_assignation', views.ClientAssignationViewSet, basename='client-assignation')
router.register(r'contract', views.ContractViewSet, basename='contract')
router.register(r'contract_assignation', views.ContractAssignationViewSet, basename='contract-assignation')
router.register(r'event', views.EventViewSet, basename='event')
router.register(r'event_assignation', views.EventAssignationViewSet, basename='event-assignation')

urlpatterns = [
    path('', include(router.urls)),
]
