# Inventory Management System

A Flask-based REST API for managing retail inventory, with CRUD operations,
OpenFoodFacts integration for product lookups, and a CLI tool for interacting
with the API.

## Features

- Flask REST API with full CRUD support (GET, POST, PATCH, DELETE)
- Integration with the OpenFoodFacts API to fetch product data by name or barcode
- CLI tool to add, view, update, delete, and search inventory items
- Unit tests using `pytest` and `unittest.mock`

## Project Structure
inventory-management-system/
├── app/
│   ├── init.py        # Flask app factory
│   ├── models.py          # In-memory inventory data + ID helper
│   ├── openfoodfacts.py   # OpenFoodFacts API integration
│   └── routes.py          # API routes (CRUD + search)
├── tests/
│   ├── init.py
│   └── test_app.py        # Unit tests
├── cli.py                 # Command-line interface
├── run.py                 # App entry point
├── Pipfile
├── Pipfile.lock
└── README.md

## Installation and Setup

1. Clone the repository:
git clone <your-repo-url>
cd inventory-management-system

2. Install dependencies (using Pipenv):
pipenv install
pipenv shell
   Or with pip:
pip install flask requests pytest

3. Run the Flask server:
python run.py
   The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint                | Description                          |
|--------|--------------------------|---------------------------------------|
| GET    | `/inventory`             | Fetch all inventory items            |
| GET    | `/inventory/<id>`        | Fetch a single item by ID            |
| POST   | `/inventory`             | Add a new item                       |
| PATCH  | `/inventory/<id>`        | Update an existing item              |
| DELETE | `/inventory/<id>`        | Delete an item                       |
| GET    | `/inventory/search`      | Look up a product on OpenFoodFacts by `name` or `barcode` query param |

### Example: Add an item
POST /inventory
Content-Type: application/json
{
"product_name": "Oat Milk",
"brands": "Oatly",
"price": 4.50,
"stock": 20
}

## CLI Usage

With the Flask server running in one terminal, use `cli.py` in another:
python cli.py list
python cli.py view 1
python cli.py add --name "Oat Milk" --brand "Oatly" --price 4.50 --stock 20
python cli.py update 1 --price 3.99 --stock 30
python cli.py delete 3
python cli.py find --name "cheddar"
python cli.py find --barcode 5000112637922

## Running Tests
pytest

Tests cover all API endpoints (including error cases) and mock external
OpenFoodFacts calls so they run without network access.

## Notes on Maintainability

- Inventory data is stored in-memory (`app/models.py`) to simulate a database,
  as specified by the assignment — swap this for a real database layer
  (e.g. SQLAlchemy) for production use.
- Each route and function includes docstrings/comments explaining its purpose.
- External API calls are isolated in `app/openfoodfacts.py` so they're easy
  to mock in tests and easy to swap out later.