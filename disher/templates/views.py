from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "disher/index.html",{})

def recepie(request , id):
    return render(request, "disher/recepie.html")