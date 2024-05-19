from django.urls import path

import user.views

urlpatterns = [
    path("main", user.views.showProducts, name="user_main"),
    path("cart", user.views.showCart),
    path('cart/purchase/', user.views.process_purchase, name='process_purchase'),
    path('cart/remove/', user.views.remove_from_cart, name='remove_from_cart'),
    path('cart/add-balance/', user.views.add_balance, name='add_balance'),
    path("transactions", user.views.showTransactions),
    path("category/<str:category>/<str:subcategory>/", user.views.showCategoryProducts),
    path('wishlist/', user.views.wishlist_view, name='wishlist'),
]
