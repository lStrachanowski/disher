from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ResetForm, ResetPasswordForm, DishForm
from .methods import CheckIfUserIsLogged, Logout_user, check_user, check_email, activate_email, reset_password
from .db import ProductOperations, DishOperations, ProductAmountOperations, DayOperations
from django.contrib import messages
from django.core.signing import Signer
from django.core import signing
from django.db import models
import json
from django.core.serializers.json import DjangoJSONEncoder
from disher.models import Day_Dish


def index(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    recepies_data = DishOperations()
    recepies_for_template = recepies_data.getAllDishes().order_by('?')[:6]
    context = {"user_status": user_status, "recepies":recepies_for_template}
    return render(request, "disher/index.html", context)


def recepie(request, slug):
    recepies_data = DishOperations()
    recepie_for_template = recepies_data.getDishData(slug)

    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)

    dish_data = DishOperations()

    amount = ProductAmountOperations()
    products = dish_data.getDish(dish_data.getDishData(slug).dish_name)
    recepie_products_amounts = amount.getAllAmounts(products)

    ingridients = recepie_products_amounts
    context = {"user_status": user_status, "recepie":recepie_for_template, "ingridients":ingridients}
    return render(request, "disher/recepie.html", context)

@login_required(login_url='/login')
def dashboard(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    user_has_recepies = True
    user_has_diet_list = True

    recepies_data = DishOperations()
    recepies_for_template = []
    recepies_for_template = recepies_data.getAllDishes().order_by('?')[:6]
    
    context = {"user_status": user_status, "user_has_recepies": user_has_recepies,
               "user_has_diet_list": user_has_diet_list, "recepies":recepies_for_template, "user_day": request.global_value}
    return render(request, "disher/dashboard.html", context)

@login_required(login_url='/login')
def daydata(request):
    day = DayOperations()
    if day.checkUserDays(request.user):
        data = day.getDayData(request.user)
        return JsonResponse(data, safe=False)
    else:
        data = {}
        data['message'] = 'No data'
        return JsonResponse(json.dumps(data), safe=False)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def add_recepie(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    if request.method == "POST":
        form = DishForm(request.POST)
        if form.is_valid():
            product_operations = ProductOperations()
            amount = ProductAmountOperations()
            products_list = request.POST.get('json_data')
            product_data = json.loads(products_list)

            product_name_list = [product_operations.findProduct(product['name']) for product in product_data]

            recepie_title = form.cleaned_data["dish_title"]
            dish_calories = form.cleaned_data["dish_calories"]
            dish_description = form.cleaned_data["dishDescription"]
            duration = form.cleaned_data["duration"]
            type_of_meal = form.cleaned_data["type_of_meal"]

            dish_operations = DishOperations()
            try:
                dish_operations.createDish(duration,type_of_meal,recepie_title, dish_calories,dish_description, request.user.username, product_name_list)
                for product in product_data:
                    amount.createAmount(product['name'] , product['amount'], product['unit'], dish_operations.getDish(recepie_title))
                messages.success(request, 'Recepie was added to database!')
            except Exception as e:
                messages.error(request, "Recepie name already exist. Check current recepie or rename your recepie")

            return HttpResponseRedirect('/message')

    return render(request, "disher/addrecepie.html", context)



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_password = form.cleaned_data["user_password"]
            user = authenticate(request, username=user_name,
                                password=user_password)
            try:
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        login_status = CheckIfUserIsLogged()
                        login_status.set_user_status_to_logged(request)
                        return redirect('/user/dashboard')
                else:
                    if check_user(user_name):
                        messages.error(
                            request, 'Password is not correct or you have not activated the account.', extra_tags="login")
                        return redirect('/login')
                    else:
                        messages.error(
                            request, 'User name and password is not correct.', extra_tags="login")
                        return redirect('/login')
            except Exception as e:
                messages.error(request, e, extra_tags="register")
                return redirect('/login')

    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/login.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_email = form.cleaned_data["user_email"]
            user_password = form.cleaned_data["user_password"]
            confirm_user_password = form.cleaned_data["confirm_user_password"]
            try:
                if check_user(user_name):
                    messages.error(
                        request, 'User name is already taken. Try other user name', extra_tags="register")
                    return redirect('/register')
                if check_email(user_email):
                    messages.error(
                        request, 'Email is already used. Try other email.', extra_tags="register")
                    return redirect('/register')
                if user_password == confirm_user_password:
                    user = User.objects.create_user(
                        user_name, user_email, user_password)
                    user.is_active = False
                    user.save()
                    signer = Signer()
                    signed_obj = signer.sign_object({"email": user_email})
                    token = signing.dumps(signed_obj)
                    print("http://127.0.0.1:8000/activate/" + token)
                    messages.success(
                        request, 'Account created. Please activate account. ')
                    return redirect('/success')
                else:
                    messages.error(
                        request, 'Passwords don`t match.', extra_tags="register")
                    return redirect('/register')
            except Exception as e:
                messages.error(request, e, extra_tags="register")
                return redirect('/register')
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/register.html", context)

@login_required(login_url='/login')
def add_meal_to_day(request, id, slug, meal_type):
    if request.method == "GET":
        data = {}
        day = DayOperations()
        dish = DishOperations()
        dish_to_add = dish.getDishData(slug)
        meal_element = dish.createDayDish(dish_to_add, meal_type)
        day_to_update = day.getDay(request.user.id)
        for current_day in day_to_update:
            if current_day.id == id:
                meal_id = day.addMealToExistingDay(id,meal_element)
                data['id'] = meal_id
                print("created", dish_to_add.dish_name, meal_type)
        return JsonResponse(json.dumps(data), safe=False)
    
@login_required(login_url='login')
def delete_meal_from_day(request, day_id, meal_id):
    if request.method == "GET":
        day = DayOperations()
        day.deleteDish(request.user.id, day_id, meal_id)
        data = {}
        data['user_id'] = request.user.id
        data['day_id'] = day_id
        data['meal_id'] = meal_id
        return JsonResponse(json.dumps(data), safe=False)
    
@login_required(login_url='login')
def delete_day(request, day_id):
    if request.method == "GET":
        day = DayOperations()
        day.deleteDay(request.user.id, day_id)
        data = {}
        data['day_id'] = day_id
        return JsonResponse(json.dumps(data), safe=False)
    
@login_required(login_url='login')
def copy_day(request, day_id):
    if request.method == "GET":
        day = DayOperations()
        json_data = day.getDayData(request.user)
        data = json.loads(json_data)
        for day in data:
            if day['day_id'] == day_id:
                return JsonResponse(json.dumps(day), safe=False)
    

@login_required(login_url='login')
def copy_dish(request, day_id, dish_id, element_id):
    if request.method == "GET":
        day = DayOperations()
        json_data = day.getDayData(request.user)
        dish_type = Day_Dish.objects.get(id = dish_id)
        data = json.loads(json_data)
        return_data = {}
        return_data['element_id'] = element_id + '-copy'
        for day in data:
            if day['day_id'] == day_id:
                for item in day['day_items']:
                    if item["dish_id"] == dish_id:
                        return_data['slug'] = item['slug']
                        return_data['name'] = item['name']
                        return_data['cal'] = item['cal']
                        return_data['type'] = dish_type.meal_type
                        return_data['day_id'] = day_id
                        return_data['new_element'] = 'true'
        return JsonResponse(json.dumps(return_data), safe=False)


def reset(request):
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            try:
                user_email = form.cleaned_data["user_email"]
                signer = Signer()
                signed_obj = signer.sign_object({"email": user_email})
                token = signing.dumps(signed_obj)
                print("http://127.0.0.1:8000/reset/" + token)
                messages.success(request, 'On your email was sent reset link.')
                return redirect('/success')
            except Exception as e:
                messages.error(request, e, extra_tags="register")
                return render(request, "disher/reset.html", context)

    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/reset.html", context)


def logout_view(request):
    logout_user = Logout_user()
    logout_user.logout(request)
    logout(request)
    return redirect("/")


def message(request):
    return render(request, "disher/message.html")


def activate(request, token):
    signer = Signer()
    token = signing.loads(token)
    obj = signer.unsign_object(token)
    try:
        if check_email(obj['email']):
            activate_email(obj['email'])
            messages.success(
                request, 'Your accourt was activatet. Please login. ')
            return redirect("/activated")
    except Exception as e:
        messages.error(request, e, extra_tags="register")
        return redirect("/activated")
    return redirect("/")


def user_activated(request):
    return render(request, "disher/activated.html")


def reset_password_view(request, token):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_password = form.cleaned_data["user_password"]
            confirm_user_password = form.cleaned_data["confirm_user_password"]
            signer = Signer()
            token = signing.loads(token)
            obj = signer.unsign_object(token)
            try:
                if user_password == confirm_user_password:
                    if check_email(obj['email']):
                        reset_password(obj['email'], user_password)
                        messages.success(
                            request, 'Yout password was changed. Please log in with new password.')
                        return redirect('/success')
                else:
                    messages.error(
                        request, 'Passwords don`t match. PLease check passwords', extra_tags="register")
            except Exception as e:
                messages.error(request, e, extra_tags="register")
                return render(request, "disher/resetPassword.html")
    return render(request, "disher/resetPassword.html")

def setDayElementId(request, id):
    try:
        request.global_value = id
        data = {'message': 'OK'}
    except Exception as e:
        data = {'message': e}
        print(e)
    return JsonResponse(data, safe=False)

        
def set_user_id_cookie(request):
    user_id = request.user.id
    response = JsonResponse({'message':'Cookie set!'})
    response.set_cookie("user_id", user_id)
    return response

def get_user_id_cookie(request):
    user_id = request.user.id
    response = JsonResponse({'id': user_id})
    return response

@login_required(login_url='/login')
def get_product_search(request, productname):
    product = ProductOperations()
    results = product.productsSearch(productname)
    data = list(results.values())
    response_data = DjangoJSONEncoder().encode(data)
    json_response_data = {'results': response_data}
    return JsonResponse(json_response_data, safe=False)

@login_required(login_url='/login')
def create_day(request):
    day_data = DayOperations()
    day_data.createDay("test", request.user)
    data = daydata(request)
    return data

@login_required(login_url='/login')  
def get_recepie_search(request, recepiename):
    data = {}
    data['dish_data'] = []
    recepie= DishOperations()
    recepie_data = recepie.findDish(recepiename)
    for recepie_item in recepie_data:
        slug = recepie_item.dish_name.replace(" ","-")
        dish_data = recepie.getDishData(slug)
        print(dish_data.dish_type)
        data['dish_data'].append({"name":recepie_item.dish_name, "preparation_time":dish_data.preparation_time, 
                                "dish_type":dish_data.dish_type, "dish_calories": dish_data.dish_calories,
                                "dish_description":dish_data.dish_description, "dish_slug":dish_data.slug, "dish_id":dish_data.id})
    return JsonResponse(data, safe=False)