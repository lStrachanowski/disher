from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50),
    calories = models.IntegerField(),
    quantity = models.IntegerField(),
    product_id = models.IntegerField()

class Dish(models.Model):
    duration = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ],
    meal = [("B", "Breakfast"),
            ("B2", "Brunch"),
            ("D", "Dinner"),
            ("D2", "Dessert"),
            ("S", "Supper")],
    preparation_time = models.CharField(max_length=1, choices=duration),
    name = models.CharField(max_length=50)
    calories = models.IntegerField(),
    dish_type = models.CharField(max_length=1, choices=meal),
    description = models.CharField(max_length=1000),
    products = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    dish_id = models.IntegerField()
    owner = models.CharField(max_length=50)

class User_Day(models.Model):
    name = models.CharField(max_length=50),
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    user_id = models.IntegerField(),
    day_id = models.IntegerField()
