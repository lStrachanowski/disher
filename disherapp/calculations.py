
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
        
    return updated_data