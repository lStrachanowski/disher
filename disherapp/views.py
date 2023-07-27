from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ResetForm
from .methods import CheckIfUserIsLogged, Logout_user, check_user, check_email
from django.contrib import messages
from django.contrib.sessions.models import Session
 


def index(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/index.html", context)


def recepie(request, id):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/recepie.html", context)


@login_required(login_url='/login')
def dashboard(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    user_has_recepies = True
    user_has_diet_list = True
    context = {"user_status": user_status, "user_has_recepies": user_has_recepies,
               "user_has_diet_list": user_has_diet_list}
    return render(request, "disher/dashboard.html", context)


def user_profil(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/profile.html", context)


def shoplist(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/shoplist.html", context)


def add_recepie(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/addrecepie.html", context)


def login_view(request):
    # Clearing messages storage
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_password = form.cleaned_data["user_password"]
            user = authenticate(request, username=user_name,
                                password=user_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    login_status = CheckIfUserIsLogged()
                    login_status.set_user_status_to_logged(request)
                    return redirect('/user/dashboard')
            else:
                if check_user(user_name):
                    messages.error(request,'Password is not correct or you have not activated the account.')
                    return redirect('/login')
                else:
                    messages.error(request,'User name and password is not correct.')
                    return redirect('/login')

    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/login.html", context)


def register(request):
    list(messages.get_messages(request))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_email = form.cleaned_data["user_email"]
            user_password = form.cleaned_data["user_password"]
            confirm_user_password = form.cleaned_data["confirm_user_password"]
            if check_user(user_name):
                messages.error(request,'User name is already taken. Try other user name')
                return redirect('/register')
            if check_email(user_email):
                messages.error(request, 'Email is not unique.' )
                return redirect('/register')
            if user_password == confirm_user_password:
                messages.success(request,'User registred please check your email to activate account.')
                # print(user_name, user_email,
                #     user_password, confirm_user_password)
                # user = User.objects.create_user(
                #     user_name, user_email, user_password)
                # user.is_active = False
                # user.save()
                return redirect('/success')  
            else:
                messages.error(request,'Passwords don`t match.')
                return redirect('/register')  
    
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/register.html", context)


def reset(request):
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["user_email"]
            print(user_email)
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/reset.html", context)


def logout_view(request):
    logout_user = Logout_user()
    logout_user.logout(request)
    logout(request)
    return redirect("/")

def success(request):
    return render(request, "disher/success.html")

def activate(request):
    print("activate")