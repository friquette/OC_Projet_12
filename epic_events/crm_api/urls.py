from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm_api import views


router = DefaultRouter()
router.register(r'client', views.ClientViewSet)
router.register(r'contract', views.ContractViewSet)
router.register(r'event', views.EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
