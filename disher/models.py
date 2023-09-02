from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_calories = models.IntegerField()
    product_quantity = models.IntegerField()
    product_protein = models.DecimalField(max_digits=5, decimal_places=2)
    product_fat = models.DecimalField(max_digits=5, decimal_places=2)
    product_carbs = models.DecimalField(max_digits=5, decimal_places=2)

class Dish(models.Model):
    dish_duration = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large")
    ]
    meal = [
        ("B", "Breakfast"),
        ("B2", "Brunch"),
        ("D", "Dinner"),
        ("D2", "Dessert"),
        ("S", "Supper")
    ]
    id = models.AutoField(primary_key=True)
    preparation_time = models.CharField(default="S", max_length=1, choices=dish_duration)
    dish_type = models.CharField(default="B", max_length=2, choices=meal)
    dish_name = models.CharField(max_length=50)
    dish_calories = models.IntegerField()
    dish_description = models.CharField(null=True, max_length=1000)
    dish_owner = models.CharField(max_length=50)
    dish_products = models.ManyToManyField(Product) 
    

class User_Day(models.Model):
    id = models.AutoField(primary_key=True)
    user_day_name = models.CharField(max_length=50)
    user_day_dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)