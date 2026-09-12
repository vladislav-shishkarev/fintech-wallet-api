from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import TransactionNotFoundError
from app.models import Transaction


async def get_transaction(session: AsyncSession, transaction_id: int) -> Transaction:
    transaction = await session.get(Transaction, transaction_id)
    if transaction is None:
        raise TransactionNotFoundError(transaction_id)
    return transaction
