from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# успешное создание юзера
def test_create_user():
    response = client.post("/users", json={"username": "alice", "age": 25})
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert body["age"] == 25
    assert isinstance(body["id"], int)


# получение существующего юзера
def test_get_existing_user():
    created = client.post("/users", json={"username": "bob", "age": 30}).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "username": "bob", "age": 30}


# получение несуществующего юзера
def test_get_missing_user():
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# удаление существующего юзера
def test_delete_user():
    created = client.post("/users", json={"username": "carol", "age": 40}).json()
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 204


# повторное удаление возвращает 404
def test_delete_twice():
    created = client.post("/users", json={"username": "dave", "age": 50}).json()
    client.delete(f"/users/{created['id']}")
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 404


# успешная валидация всех полей
def test_validation_ok():
    response = client.post(
        "/validation/users",
        json={
            "username": "eve",
            "age": 25,
            "email": "eve@gmail.com",
            "password": "bfhsa1234567",
        },
    )
    assert response.status_code == 200
    assert response.json()["user"]["phone"] == "Unknown"


# ошибка валидации возраста
def test_validation_underage():
    response = client.post(
        "/validation/users",
        json={
            "username": "kid",
            "age": 17,
            "email": "kid@gmail.com",
            "password": "fdmdfjjdkm",
        },
    )
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_failed"
    assert any(i["field"] == "age" for i in body["issues"])


# ошибка короткого пароля
def test_validation_short_password():
    response = client.post(
        "/validation/users",
        json={
            "username": "frank",
            "age": 25,
            "email": "frank@gmail.com",
            "password": "fdre",
        },
    )
    assert response.status_code == 422


# ошибка несуществующего товара
def test_item_not_found():
    response = client.get("/errors/items/9999")
    assert response.status_code == 404
    assert response.json() == {
        "error": "item_not_found",
        "detail": "Item with id 9999 does not exist",
    }


# ошибка нехватки на складе
def test_insufficient_stock():
    response = client.post("/errors/buy/2", params={"quantity": 5})
    assert response.status_code == 409
    assert response.json()["error"] == "insufficient_stock"
