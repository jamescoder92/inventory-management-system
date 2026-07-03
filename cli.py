import argparse
import requests

BASE_URL = "http://127.0.0.1:5000"


def list_items():
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        if not items:
            print("Inventory is empty.")
        for item in items:
            print(f"[{item['id']}] {item['product_name']} - "
                  f"{item.get('brands', 'N/A')} | "
                  f"${item.get('price', 0)} | stock: {item.get('stock', 0)}")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def view_item(item_id):
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.json().get('error')}")


def add_item(name, brand, ingredients, price, stock):
    payload = {
        "product_name": name,
        "brands": brand or "",
        "ingredients_text": ingredients or "",
        "price": price or 0.0,
        "stock": stock or 0
    }
    response = requests.post(f"{BASE_URL}/inventory", json=payload)
    if response.status_code == 201:
        print("Item added:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.json().get('error')}")


def update_item(item_id, price=None, stock=None):
    payload = {}
    if price is not None:
        payload["price"] = price
    if stock is not None:
        payload["stock"] = stock

    if not payload:
        print("Nothing to update. Provide --price and/or --stock.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
    if response.status_code == 200:
        print("Item updated:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.json().get('error')}")


def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print(f"Error: {response.status_code} - {response.json().get('error')}")


def find_item(name=None, barcode=None):
    params = {}
    if name:
        params["name"] = name
    if barcode:
        params["barcode"] = barcode

    if not params:
        print("Provide --name or --barcode to search.")
        return

    response = requests.get(f"{BASE_URL}/inventory/search", params=params)
    if response.status_code == 200:
        print("Found on OpenFoodFacts:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.json().get('error')}")


def main():
    parser = argparse.ArgumentParser(description="Inventory Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all inventory items")

    view_parser = subparsers.add_parser("view", help="View a single item")
    view_parser.add_argument("id", type=int)

    add_parser = subparsers.add_parser("add", help="Add a new item")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--brand", default="")
    add_parser.add_argument("--ingredients", default="")
    add_parser.add_argument("--price", type=float, default=0.0)
    add_parser.add_argument("--stock", type=int, default=0)

    update_parser = subparsers.add_parser("update", help="Update price or stock")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--price", type=float)
    update_parser.add_argument("--stock", type=int)

    delete_parser = subparsers.add_parser("delete", help="Delete an item")
    delete_parser.add_argument("id", type=int)

    search_parser = subparsers.add_parser("find", help="Find a product on OpenFoodFacts")
    search_parser.add_argument("--name")
    search_parser.add_argument("--barcode")

    args = parser.parse_args()

    if args.command == "list":
        list_items()
    elif args.command == "view":
        view_item(args.id)
    elif args.command == "add":
        add_item(args.name, args.brand, args.ingredients, args.price, args.stock)
    elif args.command == "update":
        update_item(args.id, args.price, args.stock)
    elif args.command == "delete":
        delete_item(args.id)
    elif args.command == "find":
        find_item(args.name, args.barcode)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()