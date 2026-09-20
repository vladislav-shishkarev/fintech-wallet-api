from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.errors import UserNotFoundError, WalletNotFoundError
from app.schemas import WalletRequest, WalletResponse
from app.services.wallet_service import create_wallet, get_wallet

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post(
    "",
    response_model=WalletResponse,
    responses={404: {"description": "Required user is not found"}},
)
async def create_new_wallet(
    wallet: WalletRequest, session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Create a new wallet
    """
    try:
        result = await create_wallet(session, wallet)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result


@router.get(
    "/{id}",
    response_model=WalletResponse,
    responses={404: {"description": "Required wallet is not found"}},
)
async def get_wallet_id(id: int, session: Annotated[AsyncSession, Depends(get_db)]):
    """
    Return wallet by id
    """
    try:
        result = await get_wallet(session, id)
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
