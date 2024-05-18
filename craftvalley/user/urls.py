from django.urls import path
import user.views

urlpatterns = [
    path("", user.views.login),
    path('add_product/', user.views.add_product, name='add_product'),
    path("main", user.views.showProducts),
    path("cart", user.views.showCart),
]