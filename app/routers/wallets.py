from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.errors import (
    BalanceOverflowError,
    NotEnoughMoneyError,
    UserNotFoundError,
    WalletNotActiveError,
    WalletNotFoundError,
)
from app.schemas import (
    TopUpRequest,
    TransactionResponse,
    WalletRequest,
    WalletResponse,
    WithdrawalRequest,
)
from app.services.transaction_service import top_up, withdrawal
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
    Create a new wallet.
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
    Return wallet by id.
    """
    try:
        result = await get_wallet(session, id)
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result


@router.post(
    "/{id}/top_up",
    response_model=TransactionResponse,
    responses={
        404: {"description": "Wallet not found"},
        409: {"description": "Wallet balance limit exceeded or wallet is not active"},
    },
)
async def wallet_top_up(
    top_up_data: TopUpRequest,
    id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Top up wallet balance.
    Currency is taken from the wallet.
    """
    try:
        result = await top_up(session, top_up_data, id)
    except (BalanceOverflowError, WalletNotActiveError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.post(
    "/{id}/withdrawal",
    response_model=TransactionResponse,
    responses={
        404: {"description": "Wallet not found"},
        409: {"description": "Wallet balance is not enough or wallet is not active"},
    },
)
async def wallet_withdrawal(
    withdrawal_data: WithdrawalRequest,
    id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Withdrawal of wallet balance.
    Currency is taken from the wallet.
    """
    try:
        result = await withdrawal(session, withdrawal_data, id)
    except (NotEnoughMoneyError, WalletNotActiveError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    except WalletNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result
