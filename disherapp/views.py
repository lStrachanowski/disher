from django.http import HttpResponse
from django.shortcuts import render


def check_if_user_is_logged():
    user_is_logged = True
    return user_is_logged

def index(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request, "disher/index.html", context)

def recepie(request , id):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request, "disher/recepie.html", context )

def dashboard(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request,"disher/dashboard.html", context)

def user_profil(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request, "disher/profile.html" ,context )