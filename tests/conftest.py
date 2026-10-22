import random
import uuid

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
        yield client


@pytest_asyncio.fixture
async def wallet_id(client: AsyncClient):
    r = await client.post(
        "/users",
        json={
            "name": "string",
            "email": f"{uuid.uuid4().hex}@example.com",
            "phone": f"{random.randint(10**10, 9 * 10**10)}",
        },
    )
    assert r.status_code == 200

    user_id = r.json()["id"]
    r = await client.post(
        "/wallets",
        json={"owner_id": user_id, "currency": "RUB", "name": "string"},
    )
    assert r.status_code == 200

    return r.json()["id"]


@pytest_asyncio.fixture
async def user(client: AsyncClient):
    r = await client.post(
        "/users",
        json={
            "name": "string",
            "email": f"{uuid.uuid4().hex}@example.com",
            "phone": f"{random.randint(10**10, 9 * 10**10)}",
        },
    )
    assert r.status_code == 200

    return r.json()
