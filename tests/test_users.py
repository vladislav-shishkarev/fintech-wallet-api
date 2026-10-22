import random
import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    email = f"{uuid.uuid4().hex}@example.com"
    phone = f"{random.randint(10**10, 9 * 10**10)}"
    response = await client.post(
        "/users",
        json={
            "name": "string",
            "email": email,
            "phone": phone,
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["phone"] == phone


@pytest.mark.asyncio
async def test_user_does_not_exist(client: AsyncClient):
    response = await client.get("/users/0")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, user: dict):
    response = await client.get(f"/users/{user['id']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_email_already_exists(client: AsyncClient, user: dict):
    response = await client.post(
        "/users",
        json={
            "name": "string",
            "email": user["email"],
            "phone": f"{random.randint(10**10, 9 * 10**10)}",
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_phone_already_exists(client: AsyncClient, user: dict):
    response = await client.post(
        "/users",
        json={
            "name": "string",
            "email": f"{uuid.uuid4().hex}@example.com",
            "phone": user["phone"],
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_wrong_email(client: AsyncClient):
    response = await client.post(
        "/users",
        json={
            "name": "string",
            "email": "abbb.sdsd@lsm",
            "phone": f"{random.randint(10**10, 9 * 10**10)}",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_wrong_phone(client: AsyncClient):
    response = await client.post(
        "/users",
        json={
            "name": "string",
            "email": f"{uuid.uuid4().hex}@example.com",
            "phone": "231223",
        },
    )

    assert response.status_code == 422
