from flask import Blueprint, request, jsonify
from app.models import inventory, get_next_id
from app.openfoodfacts import fetch_product_data

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


@inventory_bp.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400

    new_item = {
        "id": get_next_id(),
        "product_name": data.get("product_name"),
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


@inventory_bp.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    for key in ["product_name", "brands", "ingredients_text", "price", "stock"]:
        if key in data:
            item[key] = data[key]

    return jsonify(item), 200


@inventory_bp.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory[:] = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200


@inventory_bp.route("/inventory/search", methods=["GET"])
def search_product():
    """Query OpenFoodFacts by product name or barcode, e.g. /inventory/search?name=almond+milk"""
    name = request.args.get("name")
    barcode = request.args.get("barcode")

    if not name and not barcode:
        return jsonify({"error": "Provide a 'name' or 'barcode' query param"}), 400

    result = fetch_product_data(name=name, barcode=barcode)
    if result is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(result), 200