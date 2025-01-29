from django.contrib.auth.models import User
from disher.models import Product, Dish, Product_Amount, User_Day, Day_Dish, User_Favourite
import json

class ProductAmountOperations:
    def createAmount(self, name, amount, unit, dish_name):
        try:
            amount = Product_Amount(product_name=name, product_amount = amount, unit = unit)
            amount.save()
            amount.dish.set([dish_name])
            amount.save()
            print("Amount created")
        except Exception as e:
            print(e)
            return
        
    def getAmount(self, dish, name):
        try:
            amount = Product_Amount.objects.filter(dish = dish)
            result = [a for a in amount if a.product_name == name]
            return result[0].product_amount
        except Exception as e:
            print(e)
            return
        
    def getAllAmounts(self, dish):
        try:
            product_list = Product_Amount.objects.filter(dish = dish)
            return [[p.product_name, int(p.product_amount), p.unit] for p in product_list]
        except Exception as e:
            print(e)
            return


class ProductOperations:
    def createProduct(self, name, calories, quantity, protein, fat, carbs):
        try:
            check_product = Product.objects.filter(product_name=name).exists()
            if check_product:
                print("Already exist")
                return
            product = Product(
                product_name=name,
                product_calories=calories,
                product_quantity=quantity,
                product_protein=protein,
                product_fat=fat,
                product_carbs=carbs)
            product.save()
            print("Product created")
        except Exception as e:
            print(e)
            return

    def findProduct(self, name):
        try:
            product = Product.objects.get(product_name=name)
            return product.id
        except Exception as e:
            print(e)
            return

    def returnProductName(self, id):
        try:
            product = Product.objects.get(id=id)
            return product.product_name
        except Exception as e:
            print(e)
            return

    def deleteProduct(self, name):
        try:
            product_id = self.findProductId(name)
            if product_id:
                product = Product.objects.get(product_id=product_id)
                product.delete()
                print("Product deleted")
            else:
                print("Product not found")
        except Exception as e:
            print(e)

    def updateProduct(self, name, calories, quantity, protein, fat, carbs):
        try:
            product_object = Product.objects.filter(product_name=name)
            if product_object:
                product_object.update(product_name=name, product_calories=calories, product_quantity=quantity,
                                      product_protein=protein, product_fat=fat, product_carbs=carbs)
                print("Product updated")
            else:
                print("Product not found")
        except Exception as e:
            print(e)
            return
        
    def productsSearch(self, productname):
        try:
            searchResults = Product.objects.filter(product_name__icontains = productname)
            return searchResults
        except Exception as e:
            print(e)
            return


class DishOperations:
    def createDish(self, preparation_time, dish_type, name, calories, description, owner, products=None):
        try:
            dish_object = Dish(
                preparation_time=preparation_time,
                dish_type=dish_type,
                dish_name=name,
                dish_calories=calories,
                dish_description=description,
                dish_owner=owner)
            dish_object.save()
            if products is not None:
                dish_object.dish_products.add(*products)
            print("Dish created")
            return
        except Exception as e:
            raise ValueError(e)
            
        
    def getDishById(self, id):
        try:
            dish_object = Dish.objects.get(id=id)
            return dish_object
        except Exception as e:
            print(e)
            return

    def getDish(self, name):
        try:
            dish_object = Dish.objects.get(dish_name=name)
            return dish_object
        except Exception as e:
            print(e)
            return
        
    def getDishData(self, slug):
        try:
            dish_object = Dish.objects.get(slug=slug)
            return dish_object
        except Exception as e:
            print(e)
            return


    def deleteDish(self, name):
        try:
            dish_object = self.getDish(name)
            if dish_object:
                dish_object.delete()
                print("Dish deleted")
            else:
                print("Dish not found")
        except Exception as e:
            print(e)

    def deleteUserDish(self, id, user_name):
        try:
            dish_object = Dish.objects.get(id=id, dish_owner=user_name)
            dish_object.delete()
            print("Dish deleted")
            return True
        except Exception as e:
            print(e)
            return False

    def getAllDishes(self):
        ADMIN_NAME = 'disher'
        try:
            all_dishes = Dish.objects.all().filter(dish_owner=ADMIN_NAME)
            return all_dishes
        except Exception as e:
            print(e)

    def createDayDish(self, dish, meal):
        try:
            dayDish = Day_Dish(dish = dish, meal_type = meal)
            dayDish.save()
            return dayDish
        except Exception as e:
            print(e)

    def getSlug(self, name):
        try:
            dish_objcet = Dish.objects.get(dish_name=name)
            return dish_objcet.slug
        except Exception as e:
            print(e)
            return
        
    def findDish(self, name):
        try:
            recepie_object = Dish.objects.filter(dish_name__icontains = name)
            print(recepie_object)
            return recepie_object
        except Exception as e:
            print(e)
            return
        
    def findUserDishes(self, user_name):
        try:
            user_recepies = Dish.objects.filter(dish_owner = user_name)
            return user_recepies
        except Exception as e:
            print(e)
            return
        



class DayOperations:
    def createDay(self, user_day_name, user_id, user_day_dish=None ):
        try:
            day_object = User_Day(user_day_name = user_day_name, user_id = user_id)
            day_object.save()
            if(user_day_dish):
                day_object.user_day_dish.add(user_day_dish)
                day_object.save()
            print("created")
        except Exception as e:
            print(e)
    
    def getDay(self, id):
        try:
            day_object = User_Day.objects.filter(user_id = id)
            return day_object
        except Exception as e:
            print(e)

    def addMeal(self,id, user_day_dish):
        try:
            day_object = User_Day.objects.get(user_id = id)
            day_object.user_day_dish.add(user_day_dish)
            print("dish added")
        except Exception as e:
            print(e)
    
    def addMealToExistingDay(self,id, user_day_dish):
        try:
            day_object = User_Day.objects.get(pk = id)
            day_object.user_day_dish.add(user_day_dish)
            print("dish added")
            return user_day_dish.id

        except Exception as e:
            print(e)
    
    def getDayData(self, id):
        try:
            results_table = []
            day_object = User_Day.objects.filter(user_id = id)
            for day in day_object:
                data_table = []
                dish_id = [p for p in day.user_day_dish.all()]
                for d in dish_id:
                    d_d = Day_Dish.objects.get(id = d.id)
                    results = DishOperations().getDishById(d_d.dish.id)
                    slug = DishOperations().getSlug(results.dish_name)
                    data = {'name':results.dish_name, 'cal':results.dish_calories, 'type': d_d.meal_type, 'slug': slug, 'dish_id': d.id}
                    data_table.append(data)
                data_object = {'day_name': day.user_day_name, 'day_items': data_table, 'day_id':day.id}
                results_table.append(data_object)
            return json.dumps(results_table)
        except Exception as e:
            print(e)


    def checkUserDays(self, id):
        try:
            day_object = User_Day.objects.filter(user_id = id)
            if day_object:
                return True
        except Exception as e:
            print(e)
    
    def deleteDay(self,id, day_id):
        try:

            user_day = User_Day.objects.get(user_id=id, id=day_id)
            user_day_dishes = user_day.user_day_dish.all()
            day = DayOperations()
            for dish in user_day_dishes:
                if dish.id:
                    day.deleteDish(id, day_id, dish.id)
            user_day.delete()
            print(f"Day with id {day_id} deleted successfully.")

        except Exception as e:
            print(e)


    def deleteDish(self, id, day_id, meal_id):
        try:
            user_day = User_Day.objects.get(user_id=id, id=day_id)
            user_day_dishes = user_day.user_day_dish.all()
            day_dish_object = Day_Dish.objects.get(id=meal_id)
            for dish in user_day_dishes:
                if dish.id == meal_id:
                    user_day.user_day_dish.remove(dish)
                    day_dish_object.delete()
                    print(f"Dish with id {meal_id} deleted successfully.")
                    break  
        except Exception as e:
            print(e)
    
    def checkIfEmpty(self, id):
        try:
            user_day = User_Day.objects.filter(user_id = id)
            return user_day.count()
        except Exception as e:
            print(e)
    
        
class FavouriteOperations:
    def saveFouvriteDish(self, user_id, slug):
        dish = DishOperations().getDishData(slug)
        favourite = User_Favourite(user_id = user_id, dish = dish)
        favourite.save()
        print("Favourite saved")

    def deleteDishFromFavourite(self, user_id, slug):
        dish = DishOperations().getDishData(slug)
        favourite = User_Favourite.objects.filter(user_id=user_id, dish = dish)
        favourite.delete()
        print("Favourite deleted")
    
    def checkIfFavourite(self, user_id, slug):
        dish = DishOperations().getDishData(slug)
        favourite = User_Favourite.objects.filter(user_id=user_id, dish = dish).exists()
        if favourite:
            print("True")
            return True
        else:
            print("False")
            return False
        
    def returnFavourites(self, user_id):
        dishes = User_Favourite.objects.filter(user_id=user_id)
        return dishes