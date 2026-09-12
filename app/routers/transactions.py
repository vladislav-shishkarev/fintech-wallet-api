from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.errors import TransactionNotFoundError
from app.models import Transaction
from app.schemas import TransactionResponse
from app.services.transaction_service import get_transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db)]
) -> Transaction:
    try:
        result = await get_transaction(session, id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
