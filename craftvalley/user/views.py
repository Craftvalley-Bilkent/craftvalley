from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    context = {
        "site_name": "CraftValley",
        "desc": "CraftValley is an online shopping website"
    }
    return render(request, "user/login.html", context=context)
