from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ResetForm, ResetPasswordForm, DishForm, ChangePassword, ChangeUserName, ChangeEmail
from .methods import CheckIfUserIsLogged, Logout_user, check_user, check_email, activate_email, reset_password
from .db import ProductOperations, DishOperations, ProductAmountOperations, DayOperations, FavouriteOperations
from django.contrib import messages
from django.core.signing import Signer
from django.core import signing
from django.db import models
import json
from django.core.serializers.json import DjangoJSONEncoder
from disher.models import Day_Dish, User_Day
from . import calculations
import time
from django.core.mail import send_mail

user_has_diet_list = False

def index(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    recepies_data = DishOperations()
    recepies_for_template = recepies_data.getAllDishes(number=6)
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

    favourite_status= FavouriteOperations().checkIfFavourite(request.user.id, slug)
    context = {"user_status": user_status, "recepie":recepie_for_template, "ingridients":ingridients, "is_favourited":favourite_status}
    return render(request, "disher/recepie.html", context)

@login_required(login_url='/login')
def dashboard(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    global user_has_recepies 
    global user_has_diet_list 
    day = DayOperations()
    if day.checkIfEmpty(request.user.id) > 0:
        user_has_diet_list = True
    else:
        user_has_diet_list = False
    recepies_data = DishOperations()
    recepies_for_template = []
    recepies_for_template = recepies_data.getAllDishes(number=6)
    favourite_for_template = []
    favourite = FavouriteOperations().returnFavourites(request.user.id)
    for element in favourite:
        favourite_for_template.append(recepies_data.getDishById(element.dish_id))

    user_dishes = recepies_data.findUserDishes(user_name = request.user.get_username())
  
    context = {"user_status": user_status, "user_dishes":user_dishes,
               "user_has_diet_list": user_has_diet_list, "recepies":recepies_for_template, "user_day": request.global_value, "favourite_list":favourite_for_template}
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
    shoplist_data = request.session.get('shoplist_data', 'default value if not found')
    context = {"user_status": user_status, "shoplist_data":shoplist_data["results"]}
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
            product_name_list = [product_operations.findProduct(product['name']).id for product in product_data]

            products_calories = [product_operations.findProduct(product['name']).product_calories for product in product_data]
        
            recepie_title = form.cleaned_data["dish_title"]
            dish_calories = count_calories(products_list, products_calories)
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
                if '1062' in str(e):
                    messages.error(request, "Recepie name already exist. Check current recepie or rename your recepie")
                else:
                    messages.error(request, e)
            return HttpResponseRedirect('/message')

    return render(request, "disher/addrecepie.html", context)



@login_required(login_url='/login')
def edit_recepie(request, slug):
    amount_operations = ProductAmountOperations()
    product_operations = ProductOperations()
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    dish_operations = DishOperations()
    dish_data = dish_operations.getDishData(slug)
    dish_name = dish_data.dish_name
    dish_preparation_time = dish_data.preparation_time
    dish_type = dish_data.dish_type
    dish_description = dish_data.dish_description
    dish_products = dish_data.dish_products.all()
    product_list = []      
    products_calories = [] 
    db_product_list = []                                                   

    products = dish_operations.getDish(dish_name)
    recepie_ingridients = amount_operations.getAllAmounts(products)
    recepie_ingridients_with_id = []

    for product in dish_products:
        for element in recepie_ingridients:
            if element[0] == product.product_name:
                product_list.append( {"id": product.id, "name": product.product_name, "calories": product.product_calories, "amount": element[1], "unit": element[2]})
                recepie_ingridients_with_id.append((product.id, element))
    if request.method == "POST":
        form = DishForm(request.POST)
        if form.is_valid():
            json_products_list = request.POST.get('json_data')
            product_data = json.loads(json_products_list)
            print("product_data_from_json", product_data)
            product_list = [] 
            for product in product_data:
                product_obj = product_operations.findProduct(product['name'])
                db_product_list = [product_operations.findProduct(product['name']).id for product in product_data]                                                  
                product_list.append({
                    "id": product_obj.id,
                    "name": product['name'],
                    "calories": product_obj.product_calories,
                    "amount": product['amount'],
                    "unit": product['unit']
            })
                products_calories.append(product_obj.product_calories)
    
            dish_data.dish_products.clear()
            dish_data.dish_name = request.POST.get('dish_title')
            dish_data.preparation_time = request.POST.get('duration')
            dish_data.dish_type = request.POST.get('type_of_meal')
            dish_data.dish_description = request.POST.get('dishDescription')
            dish_data.dish_calories = count_calories(json_products_list, products_calories)
            dish_data.dish_products.add(*db_product_list)
            dish_data.save()
            
            amount_operations.deleteAllAmounts(dish_data)
            for product in product_list:
                amount_operations.createAmount(product['name'] , product['amount'], product['unit'], dish_operations.getDish(request.POST.get('dish_title')))

            return redirect('/recepie/'+ slug)


    context = {"user_status": user_status, "dish_name": dish_name,
               "dish_preparation_time": dish_preparation_time, "dish_type": dish_type, "dish_description":dish_description, "recepie_ingridients":recepie_ingridients_with_id, "slug": slug, "json_data":json.dumps(product_list) }
    return render(request, "disher/editDish.html", context)


def count_calories(products, product_calories):
    unit_matrice = {'kg': 1000, 'gr': 1, 'ml': 1}
    product_list = json.loads(products)
    calories_sum = 0
    for product, calories in zip(product_list, product_calories):
        product_amount = float(product['amount'])  # Ensure numeric type
        product_unit = product['unit']  
        if product_unit in unit_matrice:
            product_amount_converted = product_amount * (unit_matrice[product_unit] / 100)    
            calories_sum += product_amount_converted * calories     
        product_number_of_calories = calories
        print(product_amount, product_number_of_calories)
    print("calories_sum", calories_sum)
    return calories_sum

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
                    host = request.get_host()
                    verification_link =  host + "/activate/" + token
                    html_message = f"Hello {user_name},\nWelcome to disherapp! To activate your account, please visit: {verification_link}\n\nBest regards,\nThe Disher Team"
                    send_mail(
                    subject='Welcome to Our App',
                    message = html_message, 
                    from_email='disherwelcomapp@gmail.com',
                    recipient_list=[user_email],
                    fail_silently=False,)

                    messages.success(
                        request, 'Account created. Please activate account. ')
                    return redirect('/message')
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
def change_user_name(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    if request.method == "POST":
        form = ChangeUserName(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            new_user_name = form.cleaned_data["new_user_name"]
            user_password = form.cleaned_data["user_password"]
            if check_user(new_user_name):
                messages.error(request, 'User name is already taken! Use other user name.', extra_tags="changename")
                return redirect('/user/profile/changename')
            else:
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    user.username = new_user_name
                    user.save()
                    messages.success(request, 'User name changed!', extra_tags="changename")
                    return redirect('/message')
                else:
                     messages.error(request, 'Wrong user name or password!', extra_tags="changename")
                     return redirect('/user/profile/changename')

            
        
    return render(request, "disher/changename.html", context)

login_required(login_url='/login')
def change_user_email(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    if request.method == "POST":
        form = ChangeEmail(request.POST)
        if form.is_valid():
            username = request.user.username
            current_email = form.cleaned_data["user_email"]
            new_email= form.cleaned_data["new_user_email"]
            password = form.cleaned_data["user_password"]
            if check_email(current_email) and check_email(new_email) != True:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    signer = Signer()
                    signed_obj = signer.sign_object({"email": new_email, "username": username})
                    token = signing.dumps(signed_obj)
                    host = request.get_host()
                    messages.success(request, 'Email changed. Please activate email. Check your email and click activate link.')
                    verification_link =  host + "/change/email/" + token
                    html_message = f"Hello,\n We are sending link to change your email in Disherapp ! To change eamil , please visit: {verification_link}\n\nBest regards,\nThe Disher Team"
                    send_mail(
                        subject='Change email',
                        message = html_message,
                        from_email='disherwelcomapp@gmail.com',
                        recipient_list=[new_email],
                        fail_silently=False,)
                    return redirect('/message')
                else:
                    messages.error(request, 'Wrong password !', extra_tags="changeemail")
                    return redirect('/user/profile/changeemail')
            else:
                messages.error(request, 'Email already exist or email is used by other person.', extra_tags="changeemail")
                return redirect('/user/profile/changeemail')



    return render(request, "disher/changeemail.html", context)

@login_required(login_url='/login')
def change_user_password(request):
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    if request.method == "POST":
        form = ChangePassword(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]
            new_password_confirmation = form.cleaned_data["new_password_confirmation"]
            username = request.user.username
            user = User.objects.get(username=username)
            if user.check_password(current_password):
                if new_password == new_password_confirmation:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed!', extra_tags="changepassowrd")
                    return redirect('/message')
                else:
                    messages.error(request, 'Passwords don`t match.', extra_tags="changepassowrd")
                    return redirect('/user/profile/changepassword')
            else:
                messages.error(request, 'Wrong current password!', extra_tags="changepassowrd")
                return redirect('/user/profile/changepassword')
    return render(request, "disher/changepassword.html", context)


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
        dayCouont = day.checkIfEmpty(request.user.id)
        if dayCouont < 1:
            global user_has_diet_list 
            user_has_diet_list = False
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
                host = request.get_host()
                verification_link =  host + "/reset/" + token
                html_message = f"Hello,\n We are sending reset link to change your password in Disherapp ! To change password , please visit: {verification_link}\n\nBest regards,\nThe Disher Team"
                send_mail(
                    subject='Reset password',
                    message = html_message,
                    from_email='disherwelcomapp@gmail.com',
                    recipient_list=[user_email],
                    fail_silently=False,)

                messages.success(request, 'On your email was sent reset link.')
                return redirect('/message')
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
    login_status = CheckIfUserIsLogged()
    user_status = login_status.get_user_status(request)
    context = {"user_status": user_status}
    return render(request, "disher/message.html", context)


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

def activate_change_email(request, token):
    signer = Signer()
    token = signing.loads(token)
    obj = signer.unsign_object(token)
    try:
        username = obj['username']
        user = User.objects.get(username=username)
        user.email = obj['email']
        user.save()
        messages.success(request, 'Email changed!', extra_tags="changeemail")
        return redirect('/message')
    except Exception as e:
        messages.error(request, e, extra_tags="register")
        return redirect("/message")

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
                        return redirect('/message')
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
def get_user_recepies(request):
    user = request.user.get_username()
    dishes = DishOperations()
    user_dishes = dishes.findUserDishes(user)
    dishes_data = list(user_dishes.values())
    data = {'user': request.user.get_username(), 'userDishes': dishes_data}
    return JsonResponse(data, safe=False)


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
    global user_has_diet_list 
    user_has_diet_list = True
    return data

def get_recepie_search(request, recepiename):
    data = {}
    data['dish_data'] = []
    recepie= DishOperations()
    if not request.user.is_authenticated:
        recepie_data = recepie.findDish(recepiename).filter(dish_owner__in=['disher'])
        for recepie_item in recepie_data:
            data['dish_data'].append({"name":recepie_item.dish_name, "preparation_time":recepie_item.preparation_time, 
                                    "dish_type":recepie_item.dish_type, "dish_calories": recepie_item.dish_calories,
                                    "dish_description":recepie_item.dish_description, "dish_slug":recepie_item.slug, "dish_id":recepie_item.id})
        return JsonResponse(data, safe=False)
    
    else:
        recepie_data = recepie.findDish(recepiename).filter(dish_owner__in=[request.user.username, 'disher'])
        for recepie_item in recepie_data:
            data['dish_data'].append({"name":recepie_item.dish_name, "preparation_time":recepie_item.preparation_time, 
                                    "dish_type":recepie_item.dish_type, "dish_calories": recepie_item.dish_calories,
                                    "dish_description":recepie_item.dish_description, "dish_slug":recepie_item.slug, "dish_id":recepie_item.id})
        return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def get_days_product_list(request, days):
    days_id = days.split(",")
    dayData = DayOperations()
    json_data = dayData.getDayData(request.user)
    data = json.loads(json_data)
    dish_data = DishOperations()
    amount = ProductAmountOperations()
    product_list = []
    for id in days_id:
        for value in data:
            if value["day_id"] == int(id):
                for item in value["day_items"]:
                    products = dish_data.getDish(dish_data.getDishData(item["slug"]).dish_name)
                    recepie_products_amounts = amount.getAllAmounts(products)
                    product_list.append(recepie_products_amounts)
    product_list = calculations.calculateShopList(product_list)
    json_response_data = {'results': product_list}
    product_list_json = json.dumps(json_response_data)
    request.session['shoplist_data'] = json_response_data
    return JsonResponse(product_list_json, safe=False)




@login_required(login_url='/login')
def add_to_favourite(request,slug):
    if request.method == "POST":
        data = {}
        data['favourite_data'] = []
        data['favourite_data'].append({"id":request.user.id , "slug":slug})
        save_favourite = FavouriteOperations()
        save_favourite.saveFouvriteDish(request.user.id, slug)
        product_list_json = json.dumps(data)
        return JsonResponse(product_list_json, safe=False)


@login_required(login_url='/login')
def remove_from_favourite(request,slug): 
    if request.method == "POST":
        data = {}
        data['favourite_data'] = []
        data['favourite_data'].append({"id":request.user.id , "slug":slug})
        save_favourite = FavouriteOperations()
        save_favourite.deleteDishFromFavourite(request.user.id, slug)
        product_list_json = json.dumps(data)
        return JsonResponse(product_list_json, safe=False)

@login_required(login_url='/login')
def delete_user_recepie(request, id):
     if request.method == "POST":
        data = {}
        dish = DishOperations()
        day_operations = DayOperations()
        dish_slug = dish.getDishById(id).slug

        # Removing dish from favourite
        remove_from_favourite = FavouriteOperations()
        remove_success = remove_from_favourite.deleteDishFromFavourite(request.user.id, dish_slug)
        if remove_success:
            data['message'] = 'Favourite deleted successfully'
        else:
            data['message'] = 'Failed to delete favourite'

        # Removing dish from day
        day_object = User_Day.objects.filter(user_id = request.user.id)
        for day in day_object:
            dish_id = [p for p in day.user_day_dish.all()]
            for d in dish_id:
                if id == d.dish_id:
                    print(day.id, d.id)
                    day_operations.deleteDish(request.user.id, day.id, d.id)

        # Removing dish from product amount
        dish_referene= dish.getDishById(id)
        amount = ProductAmountOperations()
        amount.deleteAllAmounts(dish_referene)

        # Removing dish from user dishes
        success = dish.deleteUserDish(id, request.user.get_username())
        if success:
            data['message'] = 'Dish deleted successfully'
        else:
            data['message'] = 'Failed to delete dish'

        


        user_dishes = dish.findUserDishes(request.user.get_username())
        dishes_data = list(user_dishes.values())
        data = {'user': request.user.get_username(), 'userDishes': dishes_data}
        product_list_json = json.dumps(data)
        return JsonResponse(product_list_json, safe=False)

@login_required(login_url='/login')
def get_user_favourites(request):
    recepies_data = DishOperations()
    favourite_for_template = []
    favourite = FavouriteOperations().returnFavourites(request.user.id)
    for element in favourite:
        dish = recepies_data.getDishById(element.dish_id)
        favourite_for_template.append({
            'dish_calories': dish.dish_calories,
            'dish_description': dish.dish_description,
            'dish_name': dish.dish_name,
            'dish_owner': dish.dish_owner,
            'dish_type': dish.dish_type,
            'id': dish.id,
            'preparation_time': dish.preparation_time,
            'slug': dish.slug
        })
    data = {'user': request.user.get_username(), 'userFavouritesDishes': favourite_for_template}
    return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def read_csv(request):
    import csv
    with open('kalorie.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  
        test_product = ProductOperations()
        for row in reader:
            print(row[2].lower(),float(row[3].replace(',', '.')),  float(row[5].replace(',', '.')), float(row[6].replace(',', '.')), float(row[7].replace(',', '.')), float(row[8].replace(',', '.'))) 
            test_product.createProduct(row[2].lower(),float(row[3].replace(',', '.')), float(row[5].replace(',', '.')), float(row[6].replace(',', '.')), float(row[7].replace(',', '.')), float(row[8].replace(',', '.')))
             
    return HttpResponse('CSV read')


@login_required(login_url='/login')
def check_dish_name(request, dish_name):
    data = {}
    data['dish_name'] = dish_name
    dish = DishOperations()
    dish_data = dish.getDish(dish_name)
    if dish_data:
        data['status'] = False
        return JsonResponse(data, safe=False)
    else:
        data['status'] = True
        return JsonResponse(data, safe=False)
    