from django.http import HttpResponse
from django.shortcuts import render


def check_if_user_is_logged():
    user_is_logged = False
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
    user_has_recepies = True
    user_has_diet_list = True
    context = {"user_status": user_status, "user_has_recepies": user_has_recepies, "user_has_diet_list": user_has_diet_list}
    return render(request,"disher/dashboard.html", context)

def user_profil(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request, "disher/profile.html" ,context )

def shoplist(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request, "disher/shoplist.html" ,context )


def add_recepie(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request, "disher/addrecepie.html" ,context )

def login(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request,"disher/login.html", context)

def register(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request,"disher/register.html", context)

def reset(request):
    user_status = check_if_user_is_logged()
    context = {"user_status": user_status}
    return render(request,"disher/reset.html", context)


