from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.errors import (
    DifferentCurrencyError,
    NotEnoughMoneyError,
    TransactionNotFoundError,
    WalletNotActiveError,
    WalletNotFoundError,
    WalletOverlapError,
)
from app.models import Transaction
from app.schemas import TransactionRequest, TransactionResponse
from app.services.transaction_service import create_transaction, get_transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "",
    response_model=TransactionResponse,
    responses={
        404: {"description": "Wallet not found"},
        400: {
            "description": "Sender and receiver wallets are the same or wallets have different currencies"
        },
        409: {
            "description": "Wallet is not active or does not have enough money for transaction"
        },
    },
)
async def create_new_transaction(
    transaction: TransactionRequest, session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Transfer money between two wallets.
    Both wallets must be active and have the same currency.
    """
    try:
        result = await create_transaction(session, transaction)
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (WalletOverlapError, DifferentCurrencyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (NotEnoughMoneyError, WalletNotActiveError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result


@router.get(
    "/{id}",
    response_model=TransactionResponse,
    responses={404: {"description": "Transaction not found"}},
)
async def get_transaction_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db)]
) -> Transaction:
    """
    Return transaction by id.
    """
    try:
        result = await get_transaction(session, id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
