from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums import (
    Currency,
    TransactionStatus,
    TransactionType,
    UserStatus,
    WalletStatus,
)


class UserRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(pattern=r"^\d{11}$")


class UserResponse(BaseModel):
    id: int
    status: UserStatus
    name: str
    email: str
    phone: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class WalletRequest(BaseModel):
    owner_id: int
    currency: Currency = Field(default=Currency.RUB)
    name: str


class WalletResponse(BaseModel):
    id: int
    owner_id: int
    status: WalletStatus
    currency: Currency
    balance: Decimal = Field(
        ge=0, max_digits=11, decimal_places=2, examples=["5000.00"]
    )
    created_at: datetime
    name: str
    model_config = ConfigDict(from_attributes=True)


class TransactionRequest(BaseModel):
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: Decimal = Field(gt=0, max_digits=11, decimal_places=2, examples=["1500.00"])
    comment: str | None = None


class TransactionResponse(BaseModel):
    id: int
    sender_wallet_id: int | None
    receiver_wallet_id: int | None
    status: TransactionStatus
    currency: Currency
    amount: Decimal = Field(gt=0, max_digits=11, decimal_places=2, examples=["1500.00"])
    type: TransactionType
    date_time: datetime
    comment: str | None = None
    model_config = ConfigDict(from_attributes=True)


class TopUpRequest(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=11, decimal_places=2, examples=["1500.00"])


class WithdrawalRequest(BaseModel): ...
