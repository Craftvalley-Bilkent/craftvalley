from django.urls import path
import user.views

urlpatterns = [
    path("", user.views.login),
    path("main", user.views.showProducts),
    path("cart", user.views.showCart),
]