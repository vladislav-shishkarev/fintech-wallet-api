from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import TransactionStatus, TransactionType, WalletStatus
from app.errors import (
    BalanceOverflowError,
    DifferentCurrencyError,
    NotEnoughMoneyError,
    TransactionNotFoundError,
    WalletNotActiveError,
    WalletOverlapError,
)
from app.models import Transaction
from app.schemas import TopUpRequest, TransactionRequest, WithdrawalRequest
from app.services.wallet_service import get_wallet_for_transaction


async def create_transaction(
    session: AsyncSession, transaction_data: TransactionRequest
) -> Transaction:
    if transaction_data.receiver_wallet_id == transaction_data.sender_wallet_id:
        raise WalletOverlapError(transaction_data.receiver_wallet_id)

    if transaction_data.receiver_wallet_id < transaction_data.sender_wallet_id:
        receiver_wallet = await get_wallet_for_transaction(
            session, transaction_data.receiver_wallet_id
        )
        sender_wallet = await get_wallet_for_transaction(
            session, transaction_data.sender_wallet_id
        )
    else:
        sender_wallet = await get_wallet_for_transaction(
            session, transaction_data.sender_wallet_id
        )
        receiver_wallet = await get_wallet_for_transaction(
            session, transaction_data.receiver_wallet_id
        )

    if receiver_wallet.status != WalletStatus.ACTIVE:
        raise WalletNotActiveError(receiver_wallet.id, receiver_wallet.status)
    elif sender_wallet.status != WalletStatus.ACTIVE:
        raise WalletNotActiveError(sender_wallet.id, sender_wallet.status)
    elif receiver_wallet.currency != sender_wallet.currency:
        raise DifferentCurrencyError(sender_wallet.currency, receiver_wallet.currency)
    elif transaction_data.amount > sender_wallet.balance:
        raise NotEnoughMoneyError(sender_wallet.id, transaction_data.amount)

    sender_wallet.balance -= transaction_data.amount
    receiver_wallet.balance += transaction_data.amount

    new_transaction = Transaction(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        status=TransactionStatus.COMPLETED,
        currency=sender_wallet.currency,
        amount=transaction_data.amount,
        comment=transaction_data.comment,
        type=TransactionType.TRANSFER,
    )

    try:
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
    except IntegrityError:
        await session.rollback()
        raise NotEnoughMoneyError(
            transaction_data.sender_wallet_id, transaction_data.amount
        )

    return new_transaction


async def get_transaction(session: AsyncSession, transaction_id: int) -> Transaction:
    transaction = await session.get(Transaction, transaction_id)
    if transaction is None:
        raise TransactionNotFoundError(transaction_id)
    return transaction


async def top_up(
    session: AsyncSession, top_up_data: TopUpRequest, receiver_wallet_id: int
) -> Transaction:
    receiver_wallet = await get_wallet_for_transaction(session, receiver_wallet_id)
    if receiver_wallet.status != WalletStatus.ACTIVE:
        raise WalletNotActiveError(receiver_wallet_id, receiver_wallet.status)

    receiver_wallet.balance += top_up_data.amount

    new_transaction = Transaction(
        receiver_wallet_id=receiver_wallet.id,
        status=TransactionStatus.COMPLETED,
        currency=receiver_wallet.currency,
        amount=top_up_data.amount,
        type=TransactionType.TOP_UP,
    )

    try:
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
    except DataError:
        await session.rollback()
        raise BalanceOverflowError(receiver_wallet_id)

    return new_transaction


async def withdrawal(
    session: AsyncSession, withdrawal_data: WithdrawalRequest, sender_wallet_id: int
) -> Transaction:
    sender_wallet = await get_wallet_for_transaction(session, sender_wallet_id)
    if sender_wallet.status != WalletStatus.ACTIVE:
        raise WalletNotActiveError(sender_wallet.id, sender_wallet.status)

    sender_wallet.balance -= withdrawal_data.amount

    new_transaction = Transaction(
        sender_wallet_id=sender_wallet.id,
        status=TransactionStatus.COMPLETED,
        currency=sender_wallet.currency,
        amount=withdrawal_data.amount,
        type=TransactionType.WITHDRAWAL,
    )

    try:
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
    except IntegrityError:
        await session.rollback()
        raise NotEnoughMoneyError(sender_wallet_id, withdrawal_data.amount)

    return new_transaction
