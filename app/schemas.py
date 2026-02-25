from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from decimal import Decimal
from app.enums import Currency, WalletStatus, TransactionStatus


class UserRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(pattern="^\d{11}$")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    created_at: datetime


class WalletRequest(BaseModel):
    owner_id: int
    currency: Currency = Field(default=Currency.RUB)
    name: str


class WalletResponse(BaseModel):
    id: int
    owner_id: int
    status: WalletStatus
    currency: Currency
    balance: Decimal = Field(ge=0)
    created_at: datetime
    name: str


class TransactionRequest(BaseModel):
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: Decimal = Field(gt=0)
    comment: str | None = None


class TransactionResponse(BaseModel):
    id: int
    sender_wallet_id: int
    receiver_wallet_id: int
    status: TransactionStatus
    currency: Currency
    amount: Decimal = Field(gt=0)
    date_time: datetime
    comment: str | None = None