from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('ban/<int:business_id>/', views.ban_business, name='ban_business'),
    path('ban_details/<int:business_id>/', views.ban_details, name='ban_details'),
]
