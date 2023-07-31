from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    calories = models.IntegerField()
    quantity = models.IntegerField()
    product_id = models.AutoField(primary_key=True)  

class Dish(models.Model):
    DURATION_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ]
    MEAL_CHOICES = [
        ("B", "Breakfast"),
        ("B2", "Brunch"),
        ("D", "Dinner"),
        ("D2", "Dessert"),
        ("S", "Supper"),
    ]
    preparation_time = models.CharField(max_length=1, choices=DURATION_CHOICES)
    name = models.CharField(max_length=50)
    calories = models.IntegerField()
    dish_type = models.CharField(max_length=2, choices=MEAL_CHOICES)  
    description = models.CharField(max_length=1000)
    products = models.ManyToManyField(Product)  
    dish_id = models.AutoField(primary_key=True)  
    owner = models.CharField(max_length=50)

class User_Day(models.Model):
    name = models.CharField(max_length=50)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)  
    user_id = models.IntegerField()
    day_id = models.AutoField(primary_key=True) 