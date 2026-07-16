{
  "info": {
    "name": "Inventory Management API",
    "description": "Complete API test collection for inventory management system",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get All Items",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://127.0.0.1:5000/inventory",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "5000",
          "path": ["inventory"]
        }
      }
    },
    {
      "name": "Get Single Item",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://127.0.0.1:5000/inventory/1",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "5000",
          "path": ["inventory", "1"]
        }
      }
    },
    {
      "name": "Add New Item",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {"mode": "raw", "raw": "{\"product_name\": \"Oat Milk\", \"brands\": \"Oatly\", \"price\": 4.50, \"stock\": 20}"},
        "url": {"raw": "http://127.0.0.1:5000/inventory", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "5000", "path": ["inventory"]}
      }
    },
    {
      "name": "Update Item",
      "request": {
        "method": "PATCH",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {"mode": "raw", "raw": "{\"price\": 3.99, \"stock\": 30}"},
        "url": {"raw": "http://127.0.0.1:5000/inventory/1", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "5000", "path": ["inventory", "1"]}
      }
    },
    {
      "name": "Delete Item",
      "request": {
        "method": "DELETE",
        "header": [],
        "url": {"raw": "http://127.0.0.1:5000/inventory/3", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "5000", "path": ["inventory", "3"]}
      }
    },
    {
      "name": "Search OpenFoodFacts",
      "request": {
        "method": "GET",
        "header": [],
        "url": {"raw": "http://127.0.0.1:5000/inventory/search?name=cheddar", "protocol": "http", "host": ["127", "0", "0", "1"], "port": "5000", "path": ["inventory", "search"], "query": [{"key": "name", "value": "cheddar"}]}
      }
    }
  ]
}