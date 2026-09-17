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


@router.post("", response_model=TransactionResponse)
async def create_new_transaction(
    transaction: TransactionRequest, session: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        result = await create_transaction(session, transaction)
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (WalletOverlapError, DifferentCurrencyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (NotEnoughMoneyError, WalletNotActiveError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result


@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db)]
) -> Transaction:
    try:
        result = await get_transaction(session, id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
