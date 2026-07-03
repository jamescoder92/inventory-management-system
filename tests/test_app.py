import pytest
from unittest.mock import patch
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_add_item(client):
    new_item = {
        "product_name": "Test Product",
        "brands": "TestBrand",
        "price": 9.99,
        "stock": 10
    }
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Product"
    assert "id" in data


def test_add_item_missing_name(client):
    response = client.post("/inventory", json={"brands": "NoName"})
    assert response.status_code == 400


def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 4.99})
    assert response.status_code == 200
    assert response.get_json()["price"] == 4.99


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1.00})
    assert response.status_code == 404


def test_delete_item(client):
    # Add an item first so we have something safe to delete
    add_response = client.post("/inventory", json={"product_name": "Delete Me"})
    item_id = add_response.get_json()["id"]

    response = client.delete(f"/inventory/{item_id}")
    assert response.status_code == 200

    # Confirm it's actually gone
    get_response = client.get(f"/inventory/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


@patch("app.routes.fetch_product_data")
def test_search_product_found(mock_fetch, client):
    mock_fetch.return_value = {
        "product_name": "Mock Product",
        "brands": "MockBrand",
        "ingredients_text": "mock ingredients"
    }
    response = client.get("/inventory/search?name=milk")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Mock Product"


@patch("app.routes.fetch_product_data")
def test_search_product_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.get("/inventory/search?name=nonexistent")
    assert response.status_code == 404


def test_search_missing_params(client):
    response = client.get("/inventory/search")
    assert response.status_code == 400