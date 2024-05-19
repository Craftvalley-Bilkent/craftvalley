from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('register_business/', views.register_business, name='register_business'),
    path('login/', views.login_view, name='login'),
    path('small_business_profile/', views.small_business_profile, name='small_business_profile'),
    path('edit_business_profile/', views.edit_business_profile, name='edit_business_profile'),
    path('logout/', views.logout_view, name='logout'),
]
