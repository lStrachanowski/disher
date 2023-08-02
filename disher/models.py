from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_calories = models.IntegerField()
    product_quantity = models.IntegerField()
    product_id = models.AutoField(primary_key=True, unique=True, blank=False, null=False)

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
    preparation_time = models.CharField(default="S", max_length=1, choices=dish_duration)
    dish_type = models.CharField(default="B", max_length=2, choices=meal)
    dish_name = models.CharField(max_length=50)
    dish_calories = models.IntegerField()
    dish_description = models.CharField(null=True, max_length=1000)
    dish_products = models.ManyToManyField(Product)  # Use ManyToManyField here
    dish_id = models.AutoField(primary_key=True)
    dish_owner = models.CharField(max_length=50)

class User_Day(models.Model):
    user_day_name = models.CharField(max_length=50)
    user_day_dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    user_id = models.IntegerField()
    day_id = models.AutoField(primary_key=True)
    