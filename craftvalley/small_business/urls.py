from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('list_products/', views.list_products, name='list_products'),
    path('update_product_amount/<int:product_id>/', views.update_product_amount, name='update_product_amount'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('balance_records', views.show_balance_records, name='business_balance_records'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)