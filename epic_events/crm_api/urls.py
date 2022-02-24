from django.urls import path
from crm_api import views


urlpatterns = [
    path('crm_api/', views.employee_list),
    path('crm_api/<int:pk>/', views.employee_detail)
]