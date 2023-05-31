from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    user_logged = True
    context = {"user_status": user_logged}
    return render(request, "disher/index.html", context)

def recepie(request , id):
    user_logged = True
    context = {"user_status": user_logged}
    return render(request, "disher/recepie.html", context )

def dashboard(request):
    user_logged = True
    context = {"user_status": user_logged}
    return render(request,"disher/dashboard.html", context)

def user_profil(request):
    user_logged = True
    context = {"user_status": user_logged}
    return render(request, "disher/profile.html" ,context )