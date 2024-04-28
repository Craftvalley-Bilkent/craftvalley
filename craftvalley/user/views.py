from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        "site_name": "CraftValley",
        "desc": "CraftValley is an online shopping website"
    }
    return render(request, "user/login.html", context=context)
