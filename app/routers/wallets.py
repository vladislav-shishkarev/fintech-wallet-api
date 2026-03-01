from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db import get_db
from app.schemas import WalletRequest, WalletResponse
from app.services.wallet_service import create_wallet, get_wallet


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("", tags=["wallets"], response_model=WalletResponse)
async def create_new_wallet(wallet: WalletRequest, session: Annotated[AsyncSession, Depends(get_db)]):
    return await create_wallet(session, wallet)


@router.get("/{id}", tags=["wallets"], response_model=WalletResponse)
async def get_wallet_id(id: int, session: Annotated[AsyncSession, Depends(get_db)]):
    return await get_wallet(session, id)