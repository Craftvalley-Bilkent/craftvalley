from django.urls import path

import user.views

urlpatterns = [
    path("", user.views.login),
    path("cart", user.views.showCart),
    path("main", user.views.showProducts),
    path("transactions", user.views.showTransactions),
]
