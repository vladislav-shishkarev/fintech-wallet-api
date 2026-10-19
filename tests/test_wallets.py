import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_wallet_not_found(client: AsyncClient):
    response = await client.get("/wallets/0")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_wallet_not_enough_money_for_withdrawal(
    client: AsyncClient, wallet_id: int
):
    r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 100})
    assert r.status_code == 200

    r = await client.post(f"/wallets/{wallet_id}/withdrawal", json={"amount": 200})
    assert r.status_code == 409

    r = await client.get(f"/wallets/{wallet_id}")
    wallet_balance = r.json()["balance"]
    assert wallet_balance == "100.00"


@pytest.mark.asyncio
async def test_wallet_money_limit_exceeded(client: AsyncClient, wallet_id: int):

    r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 10**9 - 1})
    assert r.status_code == 200

    response = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 10})
    assert response.status_code == 409

    r = await client.get(f"/wallets/{wallet_id}")
    wallet_balance = r.json()["balance"]
    assert wallet_balance == "999999999.00"


@pytest.mark.asyncio
async def test_get_wallet(client: AsyncClient, wallet_id: int):

    response = await client.get(f"/wallets/{wallet_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_wrong_top_up_sum(client: AsyncClient, wallet_id: int):

    response = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": "abc"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_entire_balance_withdrawal(client: AsyncClient, wallet_id: int):

    r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 100})
    assert r.status_code == 200

    r = await client.post(f"/wallets/{wallet_id}/withdrawal", json={"amount": 100})
    assert r.status_code == 200

    r = await client.get(f"/wallets/{wallet_id}")
    wallet_balance = r.json()["balance"]
    assert wallet_balance == "0.00"


@pytest.mark.asyncio
async def test_successful_top_up(client: AsyncClient, wallet_id: int):

    r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 10})
    assert r.status_code == 200

    r = await client.get(f"/wallets/{wallet_id}")
    wallet_balance = r.json()["balance"]
    assert wallet_balance == "10.00"


@pytest.mark.asyncio
async def test_successful_withdrawal(client: AsyncClient, wallet_id: int):

    r = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 100})
    assert r.status_code == 200

    r = await client.post(f"/wallets/{wallet_id}/withdrawal", json={"amount": 10})
    assert r.status_code == 200

    r = await client.get(f"/wallets/{wallet_id}")
    wallet_balance = r.json()["balance"]
    assert wallet_balance == "90.00"


@pytest.mark.asyncio
async def test_wallet_not_active(client: AsyncClient, wallet_id: int):
    r = await client.patch(f"/wallets/{wallet_id}/status", json={"status": "blocked"})
    assert r.status_code == 200

    response = await client.post(f"/wallets/{wallet_id}/top_up", json={"amount": 10})
    assert response.status_code == 409

    r = await client.get(f"/wallets/{wallet_id}")
    wallet_balance = r.json()["balance"]
    assert wallet_balance == "0.00"
