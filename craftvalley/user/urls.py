from django.urls import path
from . import views  # Ensure this import statement is correct

urlpatterns = [
    path("", user.views.login),
    path("main", user.views.showProducts),
    path("cart", user.views.showCart),
]
