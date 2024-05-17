from django.urls import path
from . import views  # Ensure this import statement is correct

urlpatterns = [
    path('', views.login, name='login'),
]
