
from .db import  DishOperations

def calculateShopList(arr):
    ingredient_list = {}
    for sublist in arr:
    # Loop through each sublist
        for ingredient in sublist:
            # Unpack the details of each ingredient
            name, quantity, unit = ingredient
            # Use the name as the key
            if name in ingredient_list:
                # Update the quantity if the ingredient is already in the dictionary
                ingredient_list[name][0] += quantity
            else:
                # Add the ingredient to the dictionary if not present
                ingredient_list[name] = [quantity, unit]
    updated_data = []
    for name, (quantity, unit) in ingredient_list.items():
        updated_data.append([name, quantity, unit])
    updated_data.sort(key=lambda x: x[1], reverse=True)   
    return updated_data


def calculateNutrition(slug,recepie_products_amounts):
    dish_data = DishOperations()
    nutirition_data = {}
    dish_products = dish_data.getDishData(slug)
    for product_amount in recepie_products_amounts:
        for product in dish_products.dish_products.all():
            if product_amount[0] == product.product_name:
                nutirition_data[product.product_name] = {
                    "protein": product_amount[1]/100 * float(product.product_protein),
                    "fat": product_amount[1]/100 * float(product.product_fat),
                    "carbs": product_amount[1]/100 * float(product.product_carbs)
                }

    # Sum all protein, fat, carbs
    total_protein = sum(item["protein"] for item in nutirition_data.values())
    total_fat = sum(item["fat"] for item in nutirition_data.values())
    total_carbs = sum(item["carbs"] for item in nutirition_data.values())

    nutrition_totals = {
        "protein": round(total_protein, 2),
        "fat": round(total_fat, 2),
        "carbs": round(total_carbs, 2)
    }
    return nutrition_totals