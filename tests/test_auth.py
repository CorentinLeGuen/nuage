import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "mypassword"
        }
        )
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    response = await client.post(
        "/token", data={
            "username": "testuser",
            "password": "mypassword"
        }
        )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_protected_route(client: AsyncClient):
    login_response = await client.post(
        "/token", data={
            "username": "testuser",
            "password": "mypassword"
        }
        )
    token = login_response.json()["access_token"]

    response = await client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
