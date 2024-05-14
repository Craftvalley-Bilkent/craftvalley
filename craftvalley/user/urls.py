from django.urls import path
from . import views  # Ensure this import statement is correct

urlpatterns = [
    path('', views.login, name='login'),
    path('profile/<int:user_id>/', views.small_business_profile, name='small_business_profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('list_products/<int:user_id>/', views.list_products, name='list_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('balance_history/<int:user_id>/', views.balance_history, name='balance_history'),
]
