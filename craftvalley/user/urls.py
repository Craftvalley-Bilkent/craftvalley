from django.urls import path

import user.views

urlpatterns = [
    path("main", user.views.showProducts, name="user_main"),
    path("cart", user.views.showCart),
    path("transactions", user.views.showTransactions),
    path("category/<str:category>/<str:subcategory>/", user.views.showCategoryProducts),
]
