"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

def create_user(client):
    response = client.post(
        "/users",
        json={"name": "Grace Hopper", "email": "grace@example.com"},
    )
    assert response.status_code == 201
    return response.json()


def create_product(client, stock_quantity=5, price=250.0):
    response = client.post(
        "/products",
        json={
            "name": "USB-C Dock",
            "description": "Desk docking station",
            "price": price,
            "stock_quantity": stock_quantity,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_purchase_reduces_user_balance_and_product_stock(client):
    user = create_user(client)
    product = create_product(client, stock_quantity=5, price=250.0)

    response = client.post(
        "/purchases",
        json={"user_id": user["id"], "product_id": product["id"], "quantity": 2},
    )

    assert response.status_code == 201
    purchase = response.json()
    assert purchase["user_id"] == user["id"]
    assert purchase["product_id"] == product["id"]
    assert purchase["quantity"] == 2
    assert purchase["total_price"] == 500.0

    updated_user = client.get(f"/users/{user['id']}").json()
    updated_product = client.get(f"/products/{product['id']}").json()

    assert updated_user["balance"] == 99500.0
    assert updated_product["stock_quantity"] == 3


def test_purchase_rejects_insufficient_stock(client):
    user = create_user(client)
    product = create_product(client, stock_quantity=1)

    response = client.post(
        "/purchases",
        json={"user_id": user["id"], "product_id": product["id"], "quantity": 2},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock available."


def test_purchase_rejects_insufficient_balance(client):
    user = create_user(client)
    product = create_product(client, stock_quantity=1, price=100001.0)

    response = client.post(
        "/purchases",
        json={"user_id": user["id"], "product_id": product["id"], "quantity": 1},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User does not have enough balance."
