from django.urls import path
import user.views

urlpatterns = [
    path("", user.views.login),
]