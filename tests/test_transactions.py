from collections.abc import Callable

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_succesful_transaction(
    make_wallet: Callable,
    get_balance: Callable,
    create_transaction: Callable,
):
    sender_wallet_id = await make_wallet("RUB", balance=10)
    receiver_wallet_id = await make_wallet("RUB")

    response = await create_transaction(sender_wallet_id, receiver_wallet_id, 5)
    assert response.status_code == 200
    assert await get_balance(sender_wallet_id) == "5.00"
    assert await get_balance(receiver_wallet_id) == "5.00"


@pytest.mark.asyncio
async def test_succesful_entire_balance_transaction(
    make_wallet: Callable,
    get_balance: Callable,
    create_transaction: Callable,
):
    sender_wallet_id = await make_wallet("RUB", balance=10)
    receiver_wallet_id = await make_wallet("RUB")

    response = await create_transaction(sender_wallet_id, receiver_wallet_id, 10)
    assert response.status_code == 200
    assert await get_balance(sender_wallet_id) == "0.00"
    assert await get_balance(receiver_wallet_id) == "10.00"


@pytest.mark.asyncio
async def test_get_transaction(
    client: AsyncClient,
    make_wallet: Callable,
    get_balance: Callable,
    create_transaction: Callable,
):
    sender_wallet_id = await make_wallet("RUB", balance=10)
    receiver_wallet_id = await make_wallet("RUB")

    r = await create_transaction(sender_wallet_id, receiver_wallet_id, 5)
    assert r.status_code == 200
    assert await get_balance(sender_wallet_id) == "5.00"
    assert await get_balance(receiver_wallet_id) == "5.00"

    response = await client.get(f"/transactions/{r.json()['id']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_transaction_does_not_exist(client: AsyncClient):
    response = await client.get("/transactions/0")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sender_wallet_does_not_exist(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    receiver_wallet_id = await make_wallet("RUB", balance=10)
    r = await create_transaction(0, receiver_wallet_id, 5)
    assert r.status_code == 404
    assert await get_balance(receiver_wallet_id) == "10.00"


@pytest.mark.asyncio
async def test_receiver_wallet_does_not_exist(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB", balance=10)
    r = await create_transaction(sender_wallet_id, 0, 5)
    assert r.status_code == 404
    assert await get_balance(sender_wallet_id) == "10.00"


@pytest.mark.asyncio
async def test_not_enough_money_for_transaction(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB")
    receiver_wallet_id = await make_wallet("RUB")

    r = await create_transaction(sender_wallet_id, receiver_wallet_id, 5)
    assert r.status_code == 409
    assert await get_balance(sender_wallet_id) == "0.00"


@pytest.mark.asyncio
async def test_same_wallet_transaction(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB", balance=10)

    r = await create_transaction(sender_wallet_id, sender_wallet_id, 5)
    assert r.status_code == 400
    assert await get_balance(sender_wallet_id) == "10.00"


@pytest.mark.asyncio
async def test_sender_wallet_is_not_active(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB", status="inactive", balance=10)
    receiver_wallet_id = await make_wallet("RUB")

    r = await create_transaction(sender_wallet_id, receiver_wallet_id, 5)
    assert r.status_code == 409
    assert await get_balance(sender_wallet_id) == "10.00"
    assert await get_balance(receiver_wallet_id) == "0.00"


@pytest.mark.asyncio
async def test_receiver_wallet_is_not_active(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB", balance=10)
    receiver_wallet_id = await make_wallet("RUB", status="inactive")

    r = await create_transaction(sender_wallet_id, receiver_wallet_id, 5)
    assert r.status_code == 409
    assert await get_balance(sender_wallet_id) == "10.00"
    assert await get_balance(receiver_wallet_id) == "0.00"


@pytest.mark.asyncio
async def test_receiver_wallet_balance_overflow(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB", balance=999999999)
    receiver_wallet_id = await make_wallet("RUB", balance=999999999)

    r = await create_transaction(sender_wallet_id, receiver_wallet_id, 999999999)
    assert r.status_code == 409
    assert await get_balance(sender_wallet_id) == "999999999.00"
    assert await get_balance(receiver_wallet_id) == "999999999.00"


@pytest.mark.asyncio
async def test_different_currencies(
    make_wallet: Callable, create_transaction: Callable, get_balance: Callable
):
    sender_wallet_id = await make_wallet("RUB", balance=10)
    receiver_wallet_id = await make_wallet("USD")

    r = await create_transaction(sender_wallet_id, receiver_wallet_id, 5)
    assert r.status_code == 400
    assert await get_balance(sender_wallet_id) == "10.00"
    assert await get_balance(receiver_wallet_id) == "0.00"
