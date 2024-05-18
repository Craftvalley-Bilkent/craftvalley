from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('ban/<int:business_id>/', views.ban_business, name='ban_business'),
    path('ban_details/<int:business_id>/', views.ban_details, name='ban_details'),
    path('popular_products/', views.popular_products, name='popular_products'),
    path('user_trends/', views.user_trends, name='user_trends'),
    path('platform_performance/', views.platform_performance, name='platform_performance'),
]
