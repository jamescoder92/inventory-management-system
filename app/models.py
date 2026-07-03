inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 3.99,
        "stock": 25
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brands": "Nature's Own",
        "ingredients_text": "Whole wheat flour, water, yeast, salt",
        "price": 2.49,
        "stock": 40
    }
]

def get_next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1