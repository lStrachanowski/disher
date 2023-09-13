from django.contrib.auth.models import User
from disher.models import Product, Dish, Product_Amount

class ProductAmountOperations:
    def createAmount(self, name, amount, dish_name):
        try:
            check_product = Product_Amount.objects.get(product_name=name)
            print("Already exist")
        except Product_Amount.DoesNotExist:
            amount = Product_Amount(product_name=name, product_amount = amount)
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
            return [[p.product_name, int(p.product_amount)] for p in product_list]
        except Exception as e:
            print(e)
            return


class ProductOperations:
    def createProduct(self, name, calories, quantity, protein, fat, carbs):
        try:
            check_product = Product.objects.get(product_name=name)
            print("Already exist")
        except Product.DoesNotExist:
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
        except Exception as e:
            print(e)
            return

    def getDish(self, name):
        try:
            dish_objcet = Dish.objects.get(dish_name=name)
            return dish_objcet
        except Exception as e:
            print(e)
            return
        
    def getDishData(self, slug):
        try:
            dish_objcet = Dish.objects.get(slug=slug)
            return dish_objcet
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

    def getAllDishes(self):
        try:
            all_dishes = Dish.objects.all()
            return all_dishes
        except Exception as e:
            print(e)

