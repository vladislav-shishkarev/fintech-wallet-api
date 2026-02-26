from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import WalletRequest
from app.models import Wallet
from app.enums import WalletStatus
from decimal import Decimal


async def create_wallet(session: AsyncSession, wallet_data: WalletRequest) -> Wallet:
    new_wallet = Wallet(
        owner_id=wallet_data.owner_id,
        currency=wallet_data.currency,
        name=wallet_data.name,
        balance=Decimal(0),
        status=WalletStatus.ACTIVE
    )

    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)
    
    return new_wallet