import random
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_wallet_not_found():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
        response = await client.get("/wallets/0")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_wallet_not_enough_money_for_withdrawal():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 100})
        assert r.status_code == 200

        response = await client.post(
            f"/wallets/{wallet_id}/withdrawal", json={"amount": 200}
        )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_wallet_money_limit_exceeded():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        r = await client.post(
            f"/wallets/{wallet_id}/top_up", json={"amount": 10**9 - 1}
        )
        assert r.status_code == 200

        response = await client.post(
            f"/wallets/{wallet_id}/top_up", json={"amount": 10}
        )

        assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_wallet():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        response = await client.get(f"/wallets/{wallet_id}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_wrong_top_up_sum():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        response = await client.post(
            f"/wallets/{wallet_id}/top_up", json={"amount": "abc"}
        )

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_entire_balance_withdrawal():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 100})
        assert r.status_code == 200

        response = await client.post(
            f"/wallets/{wallet_id}/withdrawal", json={"amount": 100}
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_successful_top_up():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        response = await client.post(
            f"/wallets/{wallet_id}/top_up", json={"amount": 10}
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_successful_withdrawal():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
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

        wallet_id = r.json()["id"]
        r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 100})
        assert r.status_code == 200

        response = await client.post(
            f"/wallets/{wallet_id}/withdrawal", json={"amount": 10}
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_wallet_not_active():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
        response = await client.get("/wallets/0")

    assert response.status_code == 404
