import requests

BASE_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"
BASE_BARCODE_URL = "https://world.openfoodfacts.org/api/v0/product"


def fetch_product_data(name=None, barcode=None):
    """
    Fetch product details from OpenFoodFacts by barcode or name.
    Returns a simplified dict, or None if not found.
    """
    try:
        if barcode:
            response = requests.get(f"{BASE_BARCODE_URL}/{barcode}.json", timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("status") != 1:
                return None
            product = data["product"]

        elif name:
            response = requests.get(
                BASE_SEARCH_URL,
                params={"search_terms": name, "search_simple": 1, "json": 1, "page_size": 1},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            products = data.get("products", [])
            if not products:
                return None
            product = products[0]
        else:
            return None

        return {
            "product_name": product.get("product_name", "Unknown"),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", "")
        }

    except requests.exceptions.RequestException:
        return None