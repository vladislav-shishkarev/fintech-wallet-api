import random
import uuid
from collections.abc import Callable
from decimal import Decimal

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


@pytest_asyncio.fixture
async def make_wallet(client: AsyncClient, get_balance: Callable):
    async def wallet_creator(currency: str, status: str = "active", balance: int = 0):
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
            json={"owner_id": user_id, "currency": currency, "name": "string"},
        )
        assert r.status_code == 200

        wallet_id = r.json()["id"]

        if balance > 0:
            r = await client.post(
                f"/wallets/{wallet_id}/top_up", json={"amount": str(balance)}
            )
            assert r.status_code == 200
            assert Decimal(await get_balance(wallet_id)) == Decimal(balance)

        if status != "active":
            r = await client.patch(
                f"/wallets/{wallet_id}/status", json={"status": status}
            )
            assert r.status_code == 200
            assert r.json()["status"] == status

        return wallet_id

    return wallet_creator


@pytest_asyncio.fixture
async def get_balance(client: AsyncClient):
    async def balance_getter(id: int):
        response = await client.get(f"/wallets/{id}")
        assert response.status_code == 200
        return response.json()["balance"]

    return balance_getter


@pytest_asyncio.fixture
async def create_transaction(client: AsyncClient):
    async def transfer(sender_wallet_id: int, receiver_wallet_id: int, amount: int):
        response = await client.post(
            "/transactions",
            json={
                "sender_wallet_id": sender_wallet_id,
                "receiver_wallet_id": receiver_wallet_id,
                "amount": amount,
            },
        )
        return response

    return transfer
