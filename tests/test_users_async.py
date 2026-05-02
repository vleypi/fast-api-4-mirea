import pytest
from httpx import ASGITransport, AsyncClient

from main import app


# асинхронный клиент для тестов
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# асинхронное создание юзера
async def test_create_user(client, faker):
    username = faker.user_name()
    age = faker.random_int(min=18, max=99)
    response = await client.post("/users", json={"username": username, "age": age})
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == username
    assert body["age"] == age
    assert body["id"] > 0


# асинхронное получение юзера
async def test_get_existing_user(client, faker):
    created = (await client.post("/users", json={"username": faker.user_name(), "age": 25})).json()
    response = await client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


# асинхронный 404 при отсутствии юзера
async def test_get_missing_user(client):
    response = await client.get("/users/424242")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# асинхронное удаление юзера
async def test_delete_user(client, faker):
    created = (await client.post("/users", json={"username": faker.user_name(), "age": 30})).json()
    response = await client.delete(f"/users/{created['id']}")
    assert response.status_code == 204


# асинхронный повторный delete
async def test_delete_twice(client, faker):
    created = (await client.post("/users", json={"username": faker.user_name(), "age": 40})).json()
    await client.delete(f"/users/{created['id']}")
    response = await client.delete(f"/users/{created['id']}")
    assert response.status_code == 404
