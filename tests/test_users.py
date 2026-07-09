"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

def test_register_and_get_user(client):
    response = client.post(
        "/users",
        json={"name": "Ada Lovelace", "email": "ada@example.com"},
    )

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["id"] == 1
    assert created_user["name"] == "Ada Lovelace"
    assert created_user["email"] == "ada@example.com"
    assert created_user["balance"] == 100000.0

    get_response = client.get(f"/users/{created_user['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created_user


def test_duplicate_user_email_is_rejected(client):
    payload = {"name": "Ada Lovelace", "email": "ada@example.com"}

    assert client.post("/users", json=payload).status_code == 201
    response = client.post("/users", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "A user with this email already exists."
