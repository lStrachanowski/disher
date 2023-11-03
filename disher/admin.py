from django.contrib import admin
from .models import Product, Dish, User_Day, Day_Dish, Product_Amount

admin.site.register(Product)
admin.site.register(Dish)
admin.site.register(User_Day)
admin.site.register(Day_Dish)
admin.site.register(Product_Amount)
