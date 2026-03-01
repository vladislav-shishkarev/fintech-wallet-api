from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.errors import UserNotFoundError, WalletNotFoundError
from app.db import get_db
from app.schemas import WalletRequest, WalletResponse
from app.services.wallet_service import create_wallet, get_wallet


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("", tags=["wallets"], response_model=WalletResponse)
async def create_new_wallet(wallet: WalletRequest, session: Annotated[AsyncSession, Depends(get_db)]):
    try:
        result = await create_wallet(session, wallet)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result


@router.get("/{id}", tags=["wallets"], response_model=WalletResponse)
async def get_wallet_id(id: int, session: Annotated[AsyncSession, Depends(get_db)]):
    try:
        result = await get_wallet(session, id)
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result