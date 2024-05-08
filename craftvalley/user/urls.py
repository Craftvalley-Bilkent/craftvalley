from django.urls import path
import user.views

urlpatterns = [
    path("", user.views.login),
    path('add_product/', views.add_product, name='add_product'),
]