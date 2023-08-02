from django.contrib.auth.models import User
from disher.models import Product

class ProductOperations:
    def createProduct(self, name, calories, quantity):
        try:
            check_product = Product.objects.get(product_name=name)
            print("Already exist")
        except Product.DoesNotExist:
            product = Product(product_name=name, product_calories=calories, product_quantity=quantity)
            product.save()
            print("Product created")
        except Exception as e:
            print(e)

    def findProductId(self, name):
        try:
            product = Product.objects.get(product_name=name)
            return product.product_id
        except Exception as e:
            print(e)

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