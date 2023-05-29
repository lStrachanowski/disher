from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    user_logged = True
    context = {"user_status": user_logged}
    return render(request, "disher/index.html", context)

def recepie(request , id):
    return render(request, "disher/recepie.html")

def dashboard(request):
    return render(request,"disher/dashboard.html", {})