from django.contrib.auth.models import User
from disher.models import Product, Dish, Product_Amount, User_Day, Day_Dish, User_Favourite
import json

class ProductAmountOperations:
    def createAmount(self, name, amount, unit, dish_name):
        """
        Creates a new Product_Amount entry and associates it with a dish.

        Args:
            name (str): Name of the product.
            amount (float): Amount of the product.
            unit (str): Unit of measurement (e.g., 'g', 'ml').
            dish_name (str): Name of the dish to associate with this product amount.

        Returns:
            None
        """

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
        """
        Retrieves the amount of a specific product in a given dish.

        Args:
            dish (Dish): The dish object.
            name (str): Name of the product.

        Returns:
            float: The amount of the product in the dish, or None if not found.
        """

        try:
            amount = Product_Amount.objects.filter(dish = dish)
            result = [a for a in amount if a.product_name == name]
            return result[0].product_amount
        except Exception as e:
            print(e)
            return
        
    def getAllAmounts(self, dish):
        """
        Retrieves all product amounts for a given dish.

        Args:
            dish (Dish): The dish object.

        Returns:
            list: A list of [product_name, product_amount, unit] for each product in the dish.
        """

        try:
            product_list = Product_Amount.objects.filter(dish = dish)
            return [[p.product_name, int(p.product_amount), p.unit] for p in product_list]
        except Exception as e:
            print(e)
            return
    
    def deleteAllAmounts(self, dish):
        """
        Deletes all Product_Amount entries associated with a given dish.

        Args:
            dish (Dish): The dish object.

        Returns:
            None
        """

        try:
            product_list = Product_Amount.objects.filter(dish = dish)
            for p in product_list:
                p.delete()
            print("All amounts deleted")
        except Exception as e:
            print(e)
            return


class ProductOperations:
    def createProduct(self, name, calories, quantity, protein, fat, carbs):
        """
        Creates a new Product entry in the database.

        Args:
            name (str): Name of the product.
            calories (float): Caloric value of the product.
            quantity (float): Quantity of the product.
            protein (float): Protein content.
            fat (float): Fat content.
            carbs (float): Carbohydrate content.

        Returns:
            None
        """

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
        """
        Finds and returns a Product object by its name.

        Args:
            name (str): Name of the product.

        Returns:
            Product: The Product object if found, else None.
        """

        try:
            product = Product.objects.get(product_name=name)
            return product
        except Exception as e:
            print(e)
            return

    def returnProductName(self, id):
        """
        Returns the name of a product given its ID.

        Args:
            id (int): Product ID.

        Returns:
            str: Product name if found, else None.
        """

        try:
            product = Product.objects.get(id=id)
            return product.product_name
        except Exception as e:
            print(e)
            return

    def findProductId(self, name):
        """
        Finds and returns the ID of a Product by its name.

        Args:
            name (str): Name of the product.

        Returns:
            int: The ID of the product if found, else None.
        """
        try:
            product = Product.objects.get(product_name=name)
            return product.id
        except Product.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    def deleteProduct(self, id):
        """
        Deletes a product from the database by its ID.
            id (int): The unique identifier of the product to delete.
        Raises:
            Exception: If the product cannot be found or deletion fails.
        """

        try:
            product = Product.objects.get(id=id)
            product.delete()
            print("Product deleted")
        except Exception as e:
            print(e)

    def updateProduct(self, name, calories, quantity, protein, fat, carbs):
        """
        Updates the details of an existing product.

        Args:
            name (str): Name of the product.
            calories (float): New caloric value.
            quantity (float): New quantity.
            protein (float): New protein content.
            fat (float): New fat content.
            carbs (float): New carbohydrate content.

        Returns:
            None
        """

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
        """
        Searches for products whose names contain the given substring.

        Args:
            productname (str): Substring to search for in product names.

        Returns:
            QuerySet: A Django QuerySet of matching Product objects.
        """

        try:
            searchResults = Product.objects.filter(product_name__icontains = productname)
            return searchResults
        except Exception as e:
            print(e)
            return


class DishOperations:
    def createDish(self, preparation_time, dish_type, name, calories, description, owner, products=None):
        """
        Creates a new dish and associates it with the given products.

        Args:
            preparation_time (int): Preparation time in minutes.
            dish_type (str): Type of the dish (e.g., 'Appetizer', 'Main Course').
            name (str): Name of the dish.
            calories (float): Caloric value of the dish.
            description (str): Description of the dish.
            owner (str): Owner of the dish (usually the user who created it).
            products (list, optional): List of product IDs to associate with the dish.

        Returns:
            None
        """

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
        """
        Retrieves a dish by its ID.

        Args:
            id (int): Dish ID.

        Returns:
            Dish: The Dish object if found, else None.
        """

        try:
            dish_object = Dish.objects.get(id=id)
            return dish_object
        except Exception as e:
            print(e)
            return

    def getDish(self, name):
        """
        Retrieves a dish by its name.

        Args:
            name (str): Name of the dish.

        Returns:
            Dish: The Dish object if found, else None.
        """

        try:
            dish_object = Dish.objects.get(dish_name=name)
            return dish_object
        except Exception as e:
            print(e)
            return
        
    def getDishData(self, slug):
        """
        Retrieves dish data by its slug.

        Args:
            slug (str): Slug of the dish.

        Returns:
            Dish: The Dish object if found, else None.
        """

        try:
            dish_object = Dish.objects.get(slug=slug)
            return dish_object
        except Exception as e:
            print(f"Dish not found for slug: {slug}")
            return None


    def deleteDish(self, name):
        """
        Deletes a dish by its name.

        Args:
            name (str): Name of the dish.

        Returns:
            None
        """

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
        """
        Deletes a user's dish by its ID and the owner's username.

        Args:
            id (int): Dish ID.
            user_name (str): Username of the dish owner.

        Returns:
            bool: True if the dish was deleted, False otherwise.
        """

        try:
            dish_object = Dish.objects.get(id=id, dish_owner=user_name)
            dish_object.delete()
            print("Dish deleted")
            return True
        except Exception as e:
            print(e)
            return False

    def getAllDishes(self, number):
        """
        Retrieves a limited number of dishes owned by the admin, in random order.

        Args:
            number (int): Number of dishes to retrieve.

        Returns:
            QuerySet: A Django QuerySet of Dish objects.
        """

        ADMIN_NAME = 'disher'
        try:
            all_dishes = Dish.objects.all().filter(dish_owner=ADMIN_NAME).order_by('?')[:number]
            return all_dishes
        except Exception as e:
            print(e)

    def createDayDish(self, dish, meal):
        """
        Creates a Day_Dish entry for a specific dish and meal type.

        Args:
            dish (Dish): The dish object.
            meal (str): The meal type (e.g., 'Breakfast', 'Lunch').

        Returns:
            Day_Dish: The created Day_Dish object.
        """

        try:
            dayDish = Day_Dish(dish = dish, meal_type = meal)
            dayDish.save()
            return dayDish
        except Exception as e:
            print(e)

    def getSlug(self, name):
        """
        Retrieves the slug of a dish by its name.

        Args:
            name (str): Name of the dish.

        Returns:
            str: The slug of the dish if found, else None.
        """

        try:
            dish_objcet = Dish.objects.get(dish_name=name)
            return dish_objcet.slug
        except Exception as e:
            print(e)
            return
        
    def findDish(self, name):
        """
        Searches for dishes whose names contain the given substring.

        Args:
            name (str): Substring to search for in dish names.

        Returns:
            QuerySet: A Django QuerySet of matching Dish objects.
        """

        try:
            recepie_object = Dish.objects.filter(dish_name__icontains = name)
            return recepie_object
        except Exception as e:
            print(e)
            return
        
    def findUserDishes(self, user_name):
        """
        Retrieves all dishes owned by a specific user.

        Args:
            user_name (str): Username of the dish owner.

        Returns:
            QuerySet: A Django QuerySet of Dish objects.
        """

        try:
            user_recepies = Dish.objects.filter(dish_owner = user_name)
            return user_recepies
        except Exception as e:
            print(e)
            return
        
    def changeDishOwner(self, old_owner, new_owner):
        """
        Changes the owner of all dishes from old_owner to new_owner.

        Args:
            old_owner (str): Current owner's username.
            new_owner (str): New owner's username.
        """

        try:
            dishes = Dish.objects.filter(dish_owner = old_owner)
            for dish in dishes:
                dish.dish_owner = new_owner
                dish.save()
            print("Owner changed")
        except Exception as e:
            print(e)
            
        

class DayOperations:
    def createDay(self, user_day_name, user_id, user_day_dish=None ):
        """
        Creates a new user day entry.

        Args:
            user_day_name (str): Name of the user day.
            user_id (int): ID of the user.
            user_day_dish (optional): Initial dish to associate with the user day.

        Returns:
            None
        """

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
        """
        Retrieves a user's day by the user ID.

        Args:
            id (int): User ID.

        Returns:
            QuerySet: A Django QuerySet of User_Day objects.
        """

        try:
            day_object = User_Day.objects.filter(user_id = id)
            return day_object
        except Exception as e:
            print(e)

    def addMeal(self,id, user_day_dish):
        """
        Adds a dish to a user's day.

        Args:
            id (int): User ID.
            user_day_dish (Day_Dish): The Day_Dish object to add.

        Returns:
            None
        """

        try:
            day_object = User_Day.objects.get(user_id = id)
            day_object.user_day_dish.add(user_day_dish)
            print("dish added")
        except Exception as e:
            print(e)
    
    def addMealToExistingDay(self,id, user_day_dish):
        """
        Adds a dish to an existing user day.

        Args:
            id (int): User ID.
            user_day_dish (Day_Dish): The Day_Dish object to add.

        Returns:
            int: The ID of the added dish.
        """

        try:
            day_object = User_Day.objects.get(pk = id)
            day_object.user_day_dish.add(user_day_dish)
            print("dish added")
            return user_day_dish.id

        except Exception as e:
            print(e)
    
    def getDayData(self, id):
        """
        Retrieves detailed data for a user's day, including dish information.

        Args:
            id (int): User ID.

        Returns:
            str: JSON-encoded string containing day data.
        """

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
            print("fefef")
            print(e)


    def checkUserDays(self, id):
        """
        Checks if a user has any days created.

        Args:
            id (int): User ID.

        Returns:
            bool: True if the user has days, False otherwise.
        """

        try:
            day_object = User_Day.objects.filter(user_id = id)
            if day_object:
                return True
        except Exception as e:
            print(e)
    
    def deleteDay(self,id, day_id):
        """
        Deletes a user day and all associated dishes.

        Args:
            id (int): User ID.
            day_id (int): Day ID to delete.

        Returns:
            None
        """

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
        """
        Deletes a dish from a user day.

        Args:
            id (int): User ID.
            day_id (int): Day ID.
            meal_id (int): Meal ID (dish ID) to delete.

        Returns:
            None
        """

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
        """
        Checks if a user's day is empty (i.e., has no dishes).

        Args:
            id (int): User ID.

        Returns:
            int: The number of dishes in the user's day.
        """

        try:
            user_day = User_Day.objects.filter(user_id = id)
            return user_day.count()
        except Exception as e:
            print(e)
    
        
class FavouriteOperations:
    def saveFouvriteDish(self, user_id, slug):
        """
        Saves a dish as a favourite for a user.

        Args:
            user_id (int): ID of the user.
            slug (str): Slug of the dish to save as favourite.

        Returns:
            None
        """

        dish = DishOperations().getDishData(slug)
        favourite = User_Favourite(user_id = user_id, dish = dish)
        favourite.save()
        print("Favourite saved")

    def deleteDishFromFavourite(self, user_id, slug):
        """
        Deletes a dish from the user's favourites.

        Args:
            user_id (int): ID of the user.
            slug (str): Slug of the dish to delete from favourites.

        Returns:
            None
        """

        dish = DishOperations().getDishData(slug)
        favourite = User_Favourite.objects.filter(user_id=user_id, dish = dish)
        favourite.delete()
        print("Favourite deleted")
    
    def checkIfFavourite(self, user_id, slug):
        """
        Checks if a dish is in the user's favourites.

        Args:
            user_id (int): ID of the user.
            slug (str): Slug of the dish to check.

        Returns:
            bool: True if the dish is a favourite, False otherwise.
        """

        dish = DishOperations().getDishData(slug)
        favourite = User_Favourite.objects.filter(user_id=user_id, dish = dish).exists()
        if favourite:
            print("True")
            return True
        else:
            print("False")
            return False
        
    def returnFavourites(self, user_id):
        """
        Retrieves all favourite dishes for a user.

        Args:
            user_id (int): ID of the user.

        Returns:
            QuerySet: A Django QuerySet of User_Favourite objects.
        """

        dishes = User_Favourite.objects.filter(user_id=user_id)
        return dishes