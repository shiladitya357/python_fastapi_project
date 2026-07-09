"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

def test_create_list_search_update_and_delete_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Mechanical Keyboard",
            "description": "Compact tactile keyboard",
            "price": 129.99,
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201
    product = response.json()
    assert product["name"] == "Mechanical Keyboard"
    assert product["stock_quantity"] == 10

    search_response = client.get("/products", params={"name": "keyboard"})

    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["id"] == product["id"]

    update_response = client.patch(
        f"/products/{product['id']}",
        json={"price": 119.99, "stock_quantity": 12},
    )

    assert update_response.status_code == 200
    updated_product = update_response.json()
    assert updated_product["price"] == 119.99
    assert updated_product["stock_quantity"] == 12

    delete_response = client.delete(f"/products/{product['id']}")

    assert delete_response.status_code == 204
    assert client.get(f"/products/{product['id']}").status_code == 404
